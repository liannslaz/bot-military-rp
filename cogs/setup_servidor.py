import discord
from discord.ext import commands

from estructura import ESTRUCTURA, HILOS_FORO, TAGS_FORO
from roles_data import ROLES
from ids_existentes import CANAL_REGLAS_ID, CANAL_MODERADOR_ID
from permisos import overwrites_categoria, overwrites_canal_especifico
from utils.embeds import embed_error


async def _obtener_o_crear_categoria(guild, nombre, overwrites):
    categoria = discord.utils.get(guild.categories, name=nombre)
    if categoria:
        try:
            await categoria.edit(overwrites=overwrites)
        except discord.Forbidden:
            return categoria, False, f"No pude actualizar permisos de la categoría **{nombre}**"
        return categoria, False, None
    try:
        nueva = await guild.create_category(nombre, overwrites=overwrites)
        return nueva, True, None
    except discord.Forbidden:
        return None, False, f"No pude crear la categoría **{nombre}** (permisos insuficientes)"
    except discord.HTTPException as e:
        return None, False, f"Error creando categoría **{nombre}**: {e}"


async def _obtener_o_crear_canal(guild, categoria, datos, overwrites):
    nombre = datos["nombre"]
    tipo = datos["tipo"]
    id_existente = datos.get("id_existente")

    try:
        canal = None
        if id_existente:
            canal = guild.get_channel(id_existente)
            if canal is None:
                try:
                    canal = await guild.fetch_channel(id_existente)
                except (discord.NotFound, discord.Forbidden):
                    canal = None

        if canal:
            # Se conserva tal cual está (no se renombra), solo se ubica y se permisiona.
            if canal.category_id != categoria.id:
                await canal.edit(category=categoria)
            if overwrites:
                await canal.edit(overwrites=overwrites)
            return canal, False, None

        existente_por_nombre = discord.utils.get(categoria.channels, name=nombre)
        if existente_por_nombre:
            if overwrites:
                await existente_por_nombre.edit(overwrites=overwrites)
            return existente_por_nombre, False, None

        if tipo == "texto":
            nuevo = await guild.create_text_channel(nombre, category=categoria, overwrites=overwrites or {})
        elif tipo == "voz":
            nuevo = await guild.create_voice_channel(nombre, category=categoria, overwrites=overwrites or {})
        elif tipo == "foro":
            nuevo = await guild.create_forum(
                nombre, category=categoria, overwrites=overwrites or {},
                available_tags=[discord.ForumTag(name=t) for t in TAGS_FORO]
            )
        else:
            return None, False, f"Tipo de canal desconocido para **{nombre}**"

        return nuevo, True, None

    except discord.Forbidden:
        return None, False, f"Sin permisos para crear/editar **{nombre}**"
    except discord.HTTPException as e:
        return None, False, f"Error de Discord con **{nombre}**: {e}"


async def _asegurar_hilos_foro(foro):
    creados = 0
    errores = []
    existentes = set()

    try:
        for hilo in foro.threads:
            existentes.add(hilo.name)
        async for hilo in foro.archived_threads(limit=100):
            existentes.add(hilo.name)
    except discord.Forbidden:
        errores.append(f"No pude leer los hilos existentes de **{foro.name}**")
    except discord.HTTPException:
        pass

    for nombre_hilo in HILOS_FORO:
        if nombre_hilo in existentes:
            continue
        try:
            await foro.create_thread(name=nombre_hilo, content=f"**{nombre_hilo}**")
            creados += 1
        except discord.Forbidden:
            errores.append(f"No pude crear el hilo **{nombre_hilo}** en **{foro.name}**")
        except discord.HTTPException as e:
            errores.append(f"Error creando hilo **{nombre_hilo}**: {e}")

    return creados, errores


async def _sincronizar_roles(guild):
    creados, reutilizados = 0, 0
    errores = []
    roles_por_nombre = {}

    # Traemos la lista REAL y actual de roles directo de la API, en vez de
    # confiar en la caché local del bot (que puede quedar desactualizada
    # entre ejecuciones y causar que se creen roles de más).
    try:
        roles_actuales = await guild.fetch_roles()
    except discord.HTTPException:
        roles_actuales = guild.roles

    mapa_nombre_a_roles = {}
    for r in roles_actuales:
        mapa_nombre_a_roles.setdefault(r.name, []).append(r)

    # Avisamos si ya existen duplicados de ejecuciones anteriores (no los
    # borramos solos, porque no está pedido eliminar roles sin instrucción
    # explícita — solo lo reportamos para que se revise a mano).
    for nombre, lista in mapa_nombre_a_roles.items():
        if len(lista) > 1 and any(d["nombre"] == nombre for d in ROLES):
            errores.append(
                f"⚠️ Ya existían {len(lista)} roles llamados **{nombre}** antes de esta ejecución — "
                f"revisalos a mano, el bot no borra roles duplicados solo"
            )

    for datos in ROLES:
        nombre = datos["nombre"]
        color = discord.Colour(int(datos["color"].lstrip("#"), 16))
        permisos_kwargs = datos.get("permisos_guild", {})
        permisos = discord.Permissions(**permisos_kwargs) if permisos_kwargs else discord.Permissions.none()

        candidatos = mapa_nombre_a_roles.get(nombre, [])
        rol_existente = candidatos[0] if candidatos else None

        if rol_existente:
            reutilizados += 1
            try:
                cambios = {}
                if rol_existente.colour.value != color.value:
                    cambios["colour"] = color
                if permisos_kwargs and rol_existente.permissions.value != permisos.value:
                    cambios["permissions"] = permisos
                if cambios:
                    await rol_existente.edit(**cambios)
            except discord.Forbidden:
                errores.append(f"No pude actualizar el rol **{nombre}** (jerarquía insuficiente)")
            roles_por_nombre[nombre] = rol_existente
        else:
            try:
                nuevo = await guild.create_role(name=nombre, colour=color, permissions=permisos, mentionable=True)
                creados += 1
                roles_por_nombre[nombre] = nuevo
                # Actualizamos el mapa local al toque para que el resto del
                # mismo run (y cualquier nombre repetido en ROLES) lo vea.
                mapa_nombre_a_roles[nombre] = [nuevo]
                if nuevo.name != nombre:
                    errores.append(
                        f"⚠️ Discord guardó el rol como **{nuevo.name}** en vez de **{nombre}** "
                        f"(puede pasar con ciertos emojis) — revisalo a mano"
                    )
            except discord.Forbidden:
                errores.append(f"No pude crear el rol **{nombre}** (permisos insuficientes)")
            except discord.HTTPException as e:
                errores.append(f"Error creando el rol **{nombre}**: {e}")

    try:
        total = len(ROLES)
        posiciones = {}
        for i, datos in enumerate(ROLES):
            rol = roles_por_nombre.get(datos["nombre"])
            if rol:
                posiciones[rol] = total - i
        if posiciones:
            await guild.edit_role_positions(positions=posiciones)
    except (discord.Forbidden, discord.HTTPException):
        errores.append(
            "No pude reordenar la jerarquía de roles — el rol del bot debe estar por encima de "
            "**👑 | Fundador** en la lista de roles del servidor. Arrastralo ahí y volvé a correr `!server`."
        )

    return creados, reutilizados, errores


async def _configurar_community(guild, canal_reglas, canal_updates):
    try:
        if "COMMUNITY" in guild.features:
            return "ya estaba habilitada"

        if not canal_reglas or not canal_updates:
            return "no se pudo — no encontré los canales de reglas/moderación configurados"

        nuevas_features = list(guild.features) + ["COMMUNITY"]
        await guild.edit(
            rules_channel=canal_reglas,
            public_updates_channel=canal_updates,
            features=nuevas_features,
        )
        return "habilitada correctamente"
    except discord.Forbidden:
        return "requiere configuración adicional (permisos insuficientes del bot)"
    except discord.HTTPException as e:
        return f"requiere configuración adicional (Discord la rechazó: {e})"
    except Exception as e:
        return f"requiere configuración adicional (error inesperado: {e})"


class SetupServidorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="server")
    @commands.check_any(
        commands.has_permissions(administrator=True),
        commands.has_permissions(manage_guild=True),
    )
    async def server(self, ctx):
        """Crea/actualiza toda la estructura del servidor de forma idempotente."""
        guild = ctx.guild
        aviso = await ctx.send("⏳ Configurando el servidor... esto puede tardar varios minutos.")

        errores = []
        categorias_creadas = 0
        canales_creados = 0
        canales_reutilizados = 0
        foros_creados = 0
        hilos_creados = 0
        canal_reglas_obj = None
        canal_moderador_obj = None

        # 1. Roles primero (los necesitamos para armar los permisos de canal)
        roles_creados, roles_reutilizados, errores_roles = await _sincronizar_roles(guild)
        errores += errores_roles

        # 2. Categorías, canales y foros
        for datos_categoria in ESTRUCTURA:
            overwrites_cat = overwrites_categoria(datos_categoria["acceso"], guild)
            categoria, fue_creada, error = await _obtener_o_crear_categoria(
                guild, datos_categoria["nombre"], overwrites_cat
            )
            if error:
                errores.append(error)
            if categoria is None:
                continue
            if fue_creada:
                categorias_creadas += 1

            for datos_canal in datos_categoria["canales"]:
                overwrites_canal = overwrites_cat
                clave_especial = datos_canal.get("acceso_canal")
                if clave_especial:
                    especifico = overwrites_canal_especifico(clave_especial, guild)
                    if especifico:
                        overwrites_canal = especifico

                canal, fue_creado, error = await _obtener_o_crear_canal(
                    guild, categoria, datos_canal, overwrites_canal
                )
                if error:
                    errores.append(error)
                    continue

                # Guardamos la referencia real a estos 2 canales (los necesita
                # Community), sin importar si se reutilizaron por ID o se
                # crearon nuevos en este mismo run.
                if datos_canal.get("id_existente") == CANAL_REGLAS_ID:
                    canal_reglas_obj = canal
                elif datos_canal.get("id_existente") == CANAL_MODERADOR_ID:
                    canal_moderador_obj = canal

                if datos_canal["tipo"] == "foro":
                    if fue_creado:
                        foros_creados += 1
                    else:
                        canales_reutilizados += 1
                    n_hilos, errores_hilos = await _asegurar_hilos_foro(canal)
                    hilos_creados += n_hilos
                    errores += errores_hilos
                else:
                    if fue_creado:
                        canales_creados += 1
                    else:
                        canales_reutilizados += 1

        # 3. Community
        estado_community = await _configurar_community(guild, canal_reglas_obj, canal_moderador_obj)

        # 4. Resumen final
        embed = discord.Embed(title="✅ Estructura configurada", color=discord.Color.green())
        embed.add_field(name="Categorías creadas", value=str(categorias_creadas), inline=True)
        embed.add_field(name="Canales creados", value=str(canales_creados), inline=True)
        embed.add_field(name="Canales reutilizados", value=str(canales_reutilizados), inline=True)
        embed.add_field(name="Foros creados", value=str(foros_creados), inline=True)
        embed.add_field(name="Hilos de curso creados", value=str(hilos_creados), inline=True)
        embed.add_field(name="Roles creados", value=str(roles_creados), inline=True)
        embed.add_field(name="Roles reutilizados", value=str(roles_reutilizados), inline=True)
        embed.add_field(name="Community", value=estado_community, inline=False)

        if errores:
            texto_errores = "\n".join(f"• {e}" for e in errores[:15])
            if len(errores) > 15:
                texto_errores += f"\n... y {len(errores) - 15} más"
            embed.add_field(name=f"⚠️ Avisos ({len(errores)})", value=texto_errores, inline=False)

        await aviso.edit(content=None, embed=embed)

    @server.error
    async def server_error(self, ctx, error):
        if isinstance(error, commands.CheckAnyFailure):
            await ctx.send(embed=embed_error("Necesitás permiso de Administrador o Gestionar Servidor para usar este comando."))
        else:
            await ctx.send(embed=embed_error(f"Ocurrió un error: {error}"))
            print(f"Error en !server: {error}")


async def setup(bot):
    await bot.add_cog(SetupServidorCog(bot))
