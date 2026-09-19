import asyncio

import discord
from discord.ext import commands

from estructura import ESTRUCTURA, HILOS_FORO, TAGS_FORO
from roles_data import ROLES
from ids_existentes import CANAL_REGLAS_ID, CANAL_MODERADOR_ID
from permisos import overwrites_categoria, overwrites_canal_especifico
from utils.embeds import embed_error


LIMITE_CAMPO_EMBED = 1024

# IDs de los canales que creó Discord al activar Comunidad en el servidor NUEVO.
# Si por algún motivo no se encuentran por ID, se usan los canales que Discord
# tiene registrados como "reglas" y "actualizaciones de la comunidad".
REGLAS_ID_NUEVO = 1551000715273568378
MODERADOR_ID_NUEVO = 1551000715273568381

_CLASES_CANAL = {
    "texto": discord.TextChannel,
    "voz": discord.VoiceChannel,
    "foro": discord.ForumChannel,
}


# ──────────────────────────────────────────────────────────────────────────
# Utilidades
# ──────────────────────────────────────────────────────────────────────────

def _recortar(texto, limite=LIMITE_CAMPO_EMBED):
    """Los campos de un embed no pueden pasar de 1024 caracteres."""
    return texto if len(texto) <= limite else texto[: limite - 1] + "…"


def _nombre_normalizado(nombre, tipo):
    """Discord guarda los canales de texto y foros en minúsculas y con guiones
    en vez de espacios. Sin esto, al volver a correr el comando no reconoce
    los canales ya creados y los duplica."""
    if tipo in ("texto", "foro"):
        return nombre.lower().replace(" ", "-")
    return nombre


def _es_reglas(id_existente):
    return id_existente is not None and id_existente in (CANAL_REGLAS_ID, REGLAS_ID_NUEVO)


def _es_moderador(id_existente):
    return id_existente is not None and id_existente in (CANAL_MODERADOR_ID, MODERADOR_ID_NUEVO)


async def _progreso(mensaje, texto):
    try:
        await mensaje.edit(content=texto)
    except discord.HTTPException:
        pass


# ──────────────────────────────────────────────────────────────────────────
# Orden de roles (Fundador = más alto ... Ciudadano = más bajo)
# ──────────────────────────────────────────────────────────────────────────

def _contiene(datos, palabra):
    return palabra in datos["nombre"].lower()


def _roles_en_orden():
    """Devuelve ROLES de mayor a menor rango (Fundador primero, Ciudadano
    último). Si en roles_data.py vinieran al revés, los invierte."""
    roles = list(ROLES)
    if len(roles) > 1 and _contiene(roles[0], "ciudadano") and _contiene(roles[-1], "fundador"):
        roles.reverse()
    return roles


def _validar_roles(roles):
    """Devuelve un texto de error si el orden no es el pedido, o None si está bien."""
    if not roles:
        return "La lista `ROLES` está vacía."
    if not _contiene(roles[0], "fundador"):
        return (
            f"El rol más alto de `ROLES` debe ser **Fundador**, pero el primero es "
            f"**{roles[0]['nombre']}**. Corregí `roles_data.py`."
        )
    if not _contiene(roles[-1], "ciudadano"):
        return (
            f"El rol más bajo de `ROLES` debe ser **Ciudadano**, pero el último es "
            f"**{roles[-1]['nombre']}**. Corregí `roles_data.py`."
        )
    nombres = [d["nombre"] for d in roles]
    repetidos = sorted({n for n in nombres if nombres.count(n) > 1})
    if repetidos:
        return "Hay roles repetidos en `ROLES`: " + ", ".join(f"**{n}**" for n in repetidos)
    return None


async def _esperar_roles_en_cache(guild, roles, intentos=20):
    """Espera a que el bot 'vea' los roles recién creados antes de armar permisos."""
    ids = [r.id for r in roles]
    for _ in range(intentos):
        if all(guild.get_role(i) is not None for i in ids):
            return True
        await asyncio.sleep(0.5)
    return False


async def _verificar_orden_roles(guild, roles_def, roles_por_nombre):
    """True si las posiciones reales van de mayor a menor siguiendo roles_def,
    False si no, None si no se pudo verificar."""
    try:
        posiciones = {r.id: r.position for r in await guild.fetch_roles()}
    except discord.HTTPException:
        return None

    reales = []
    for datos in roles_def:
        rol = roles_por_nombre.get(datos["nombre"])
        if rol is None:
            continue
        pos = posiciones.get(rol.id)
        if pos is None:
            return False
        reales.append(pos)
    return all(reales[i] > reales[i + 1] for i in range(len(reales) - 1))


async def _sincronizar_roles(guild, roles_def):
    creados, reutilizados = 0, 0
    errores = []
    roles_por_nombre = {}
    nombres_definidos = {d["nombre"] for d in roles_def}

    # Lista REAL y actual de roles directo de la API, no la caché local.
    try:
        roles_actuales = await guild.fetch_roles()
    except discord.HTTPException:
        roles_actuales = guild.roles

    mapa_nombre_a_roles = {}
    for r in roles_actuales:
        mapa_nombre_a_roles.setdefault(r.name, []).append(r)

    # Avisamos de duplicados previos (no se borran solos).
    for nombre, lista in mapa_nombre_a_roles.items():
        if len(lista) > 1 and nombre in nombres_definidos:
            errores.append(
                f"⚠️ Ya existían {len(lista)} roles llamados **{nombre}** antes de esta ejecución — "
                f"revisalos a mano, el bot no borra roles duplicados solo"
            )

    for datos in roles_def:
        nombre = datos["nombre"]

        try:
            color = discord.Colour(int(datos["color"].lstrip("#"), 16))
        except (ValueError, KeyError, AttributeError):
            color = discord.Colour.default()
            errores.append(f"Color inválido en el rol **{nombre}** — se usó el color por defecto")

        permisos_kwargs = datos.get("permisos_guild", {})
        try:
            permisos = discord.Permissions(**permisos_kwargs) if permisos_kwargs else discord.Permissions.none()
        except TypeError as e:
            permisos = discord.Permissions.none()
            permisos_kwargs = {}
            errores.append(f"Permisos inválidos en el rol **{nombre}** ({e}) — se creó sin permisos")

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
            except discord.HTTPException as e:
                errores.append(f"Error actualizando el rol **{nombre}**: {e}")
            roles_por_nombre[nombre] = rol_existente
        else:
            try:
                nuevo = await guild.create_role(name=nombre, colour=color, permissions=permisos, mentionable=True)
                creados += 1
                roles_por_nombre[nombre] = nuevo
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

    # Esperamos a que el bot vea todos los roles antes de seguir.
    await _esperar_roles_en_cache(guild, list(roles_por_nombre.values()))

    # Jerarquía: el primero de la lista (Fundador) queda arriba de todo,
    # el último (Ciudadano) abajo de todo.
    orden_ok = None
    try:
        total = len(roles_def)
        posiciones = {}
        for i, datos in enumerate(roles_def):
            rol = roles_por_nombre.get(datos["nombre"])
            if rol:
                posiciones[rol] = total - i
        if posiciones:
            await guild.edit_role_positions(positions=posiciones)
            orden_ok = await _verificar_orden_roles(guild, roles_def, roles_por_nombre)
            if orden_ok is False:
                errores.append(
                    "⚠️ La jerarquía de roles no quedó en el orden esperado — el rol del bot debe "
                    "estar por encima de **Fundador**. Arrastralo ahí y volvé a correr `!server`."
                )
    except (discord.Forbidden, discord.HTTPException):
        orden_ok = False
        errores.append(
            "No pude reordenar la jerarquía de roles — el rol del bot debe estar por encima de "
            "**Fundador** en la lista de roles del servidor. Arrastralo ahí y volvé a correr `!server`."
        )
    except AttributeError:
        orden_ok = False
        errores.append("No pude reordenar los roles: hace falta discord.py 2.4 o superior (`Guild.edit_role_positions`).")

    await asyncio.sleep(1)  # margen para que la caché del bot se ponga al día
    return creados, reutilizados, orden_ok, errores


# ──────────────────────────────────────────────────────────────────────────
# Categorías, canales y foros
# ──────────────────────────────────────────────────────────────────────────

async def _obtener_o_crear_categoria(guild, nombre, overwrites):
    categoria = discord.utils.get(guild.categories, name=nombre)
    if categoria:
        try:
            await categoria.edit(overwrites=overwrites)
        except discord.Forbidden:
            return categoria, False, f"No pude actualizar permisos de la categoría **{nombre}**"
        except discord.HTTPException as e:
            return categoria, False, f"Error actualizando la categoría **{nombre}**: {e}"
        return categoria, False, None
    try:
        nueva = await guild.create_category(nombre, overwrites=overwrites)
        return nueva, True, None
    except discord.Forbidden:
        return None, False, f"No pude crear la categoría **{nombre}** (permisos insuficientes)"
    except discord.HTTPException as e:
        return None, False, f"Error creando categoría **{nombre}**: {e}"


async def _obtener_o_crear_canal(guild, categoria, datos, overwrites, canal_reglas, canal_updates):
    nombre = datos["nombre"]
    tipo = datos["tipo"]
    clase = _CLASES_CANAL.get(tipo)
    if clase is None:
        return None, False, f"Tipo de canal desconocido ('{tipo}') para **{nombre}**"

    nombre_discord = _nombre_normalizado(nombre, tipo)
    id_existente = datos.get("id_existente")

    try:
        canal = None
        es_de_community = False

        # Los canales de reglas y moderación son los que creó Discord al
        # activar Comunidad en ESTE servidor. Se toman directo de ahí (los IDs
        # de otro servidor no sirven). Cualquier otro id_existente se busca
        # solo dentro de este servidor.
        if id_existente is not None:
            if _es_reglas(id_existente):
                canal, es_de_community = canal_reglas, True
            elif _es_moderador(id_existente):
                canal, es_de_community = canal_updates, True
            else:
                canal = guild.get_channel(id_existente)

        if canal is not None:
            if not isinstance(canal, clase):
                return None, False, f"**{nombre}**: el canal existente no es de tipo {tipo}"
            # Se ubica al final de su categoría (así respeta el orden de ESTRUCTURA).
            if canal.category_id != categoria.id:
                await canal.move(end=True, category=categoria, sync_permissions=False)
            cambios = {}
            # Solo los canales que creó Discord con nombre genérico se renombran.
            if es_de_community and canal.name not in (nombre, nombre_discord):
                cambios["name"] = nombre
            if overwrites:
                cambios["overwrites"] = overwrites
            if cambios:
                await canal.edit(**cambios)
            return canal, False, None

        existente_por_nombre = next(
            (c for c in categoria.channels if isinstance(c, clase) and c.name in (nombre, nombre_discord)),
            None,
        )
        if existente_por_nombre:
            if overwrites:
                await existente_por_nombre.edit(overwrites=overwrites)
            return existente_por_nombre, False, None

        if tipo == "texto":
            nuevo = await guild.create_text_channel(nombre, category=categoria, overwrites=overwrites or {})
        elif tipo == "voz":
            nuevo = await guild.create_voice_channel(nombre, category=categoria, overwrites=overwrites or {})
        else:  # foro
            nuevo = await guild.create_forum(
                nombre, category=categoria, overwrites=overwrites or {},
                available_tags=[discord.ForumTag(name=t) for t in TAGS_FORO]
            )

        return nuevo, True, None

    except discord.Forbidden:
        return None, False, f"Sin permisos para crear/editar **{nombre}**"
    except discord.HTTPException as e:
        return None, False, f"Error de Discord con **{nombre}**: {e}"
    except Exception as e:
        return None, False, f"Error inesperado con **{nombre}**: {e}"


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


# ──────────────────────────────────────────────────────────────────────────
# Cog
# ──────────────────────────────────────────────────────────────────────────

class SetupServidorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._en_curso = set()  # servidores donde ya hay un !server corriendo

    @commands.command(name="server")
    @commands.guild_only()
    @commands.check_any(
        commands.has_permissions(administrator=True),
        commands.has_permissions(manage_guild=True),
    )
    async def server(self, ctx):
        """Crea/actualiza toda la estructura del servidor de forma idempotente.

        Requisito: activar Comunidad ANTES de correr el comando (los foros solo
        existen en servidores con Comunidad, y Discord crea ahí los canales de
        reglas y moderación que se reutilizan)."""
        guild = ctx.guild

        if guild.id in self._en_curso:
            await ctx.send("⏳ Ya hay una configuración corriendo en este servidor. Esperá a que termine.")
            return

        # ── Validaciones previas: si algo falla, no se toca nada ──────────
        roles_def = _roles_en_orden()
        problema = _validar_roles(roles_def)
        if problema:
            await ctx.send(embed=embed_error(problema))
            return

        yo = guild.me
        if yo is None or not yo.guild_permissions.administrator:
            await ctx.send(embed=embed_error(
                "El bot necesita el permiso de **Administrador** para armar el servidor. "
                "Dáselo a su rol y volvé a correr `!server`."
            ))
            return

        if "COMMUNITY" not in guild.features:
            await ctx.send(embed=embed_error(
                "Primero activá **Comunidad** en Configuración del servidor → Habilitar comunidad "
                "(terminá el asistente de Discord) y después volvé a correr `!server`."
            ))
            return

        canal_reglas = guild.get_channel(REGLAS_ID_NUEVO) or guild.rules_channel
        canal_updates = guild.get_channel(MODERADOR_ID_NUEVO) or guild.public_updates_channel
        if not isinstance(canal_reglas, discord.TextChannel) or not isinstance(canal_updates, discord.TextChannel):
            await ctx.send(embed=embed_error(
                f"No encontré los canales de reglas (`{REGLAS_ID_NUEVO}`) y moderación "
                f"(`{MODERADOR_ID_NUEVO}`) en este servidor. ¿Estás corriendo `!server` en el servidor correcto?"
            ))
            return

        self._en_curso.add(guild.id)
        try:
            aviso = await ctx.send("⏳ Configurando el servidor... esto puede tardar varios minutos.")

            errores = []
            categorias_creadas = 0
            canales_creados = 0
            canales_reutilizados = 0
            foros_creados = 0
            hilos_creados = 0
            canal_reglas_obj = None
            canal_moderador_obj = None
            ids_estructura = set()

            # 1. Roles primero (se necesitan para armar los permisos de canal)
            await _progreso(aviso, "⏳ Paso 1/2: creando y ordenando roles...")
            roles_creados, roles_reutilizados, orden_roles, errores_roles = await _sincronizar_roles(guild, roles_def)
            errores += errores_roles

            # 2. Categorías, canales y foros (en el orden de ESTRUCTURA)
            await _progreso(aviso, "⏳ Paso 2/2: creando categorías, canales y foros...")
            for datos_categoria in ESTRUCTURA:
                try:
                    overwrites_cat = overwrites_categoria(datos_categoria["acceso"], guild)
                except Exception as e:
                    errores.append(f"No pude armar los permisos de la categoría **{datos_categoria.get('nombre')}**: {e}")
                    continue

                categoria, fue_creada, error = await _obtener_o_crear_categoria(
                    guild, datos_categoria["nombre"], overwrites_cat
                )
                if error:
                    errores.append(error)
                if categoria is None:
                    continue
                ids_estructura.add(categoria.id)
                if fue_creada:
                    categorias_creadas += 1

                for datos_canal in datos_categoria["canales"]:
                    overwrites_canal = overwrites_cat
                    clave_especial = datos_canal.get("acceso_canal")
                    if clave_especial:
                        try:
                            especifico = overwrites_canal_especifico(clave_especial, guild)
                        except Exception as e:
                            errores.append(f"No pude armar los permisos del canal **{datos_canal['nombre']}**: {e}")
                            continue
                        if especifico:
                            overwrites_canal = especifico

                    canal, fue_creado, error = await _obtener_o_crear_canal(
                        guild, categoria, datos_canal, overwrites_canal, canal_reglas, canal_updates
                    )
                    if error:
                        errores.append(error)
                        continue
                    ids_estructura.add(canal.id)

                    ide = datos_canal.get("id_existente")
                    if _es_reglas(ide):
                        canal_reglas_obj = canal
                    elif _es_moderador(ide):
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

            if canal_reglas_obj is None:
                errores.append(
                    "No se acomodó el canal de reglas de Comunidad: revisá que en ESTRUCTURA exista "
                    "una entrada con `id_existente` = CANAL_REGLAS_ID"
                )
            if canal_moderador_obj is None:
                errores.append(
                    "No se acomodó el canal de moderación de Comunidad: revisá que en ESTRUCTURA exista "
                    "una entrada con `id_existente` = CANAL_MODERADOR_ID"
                )

            # Canales/categorías que no son de la estructura (p. ej. los que
            # trae Discord por defecto). Solo se informan, no se borran.
            sobrantes = [c.name for c in guild.channels if c.id not in ids_estructura]

            # ── Resumen final ──────────────────────────────────────────────
            if errores:
                embed = discord.Embed(title="⚠️ Estructura configurada con avisos", color=discord.Color.orange())
            else:
                embed = discord.Embed(title="✅ Estructura configurada", color=discord.Color.green())

            embed.add_field(name="Categorías creadas", value=str(categorias_creadas), inline=True)
            embed.add_field(name="Canales creados", value=str(canales_creados), inline=True)
            embed.add_field(name="Canales reutilizados", value=str(canales_reutilizados), inline=True)
            embed.add_field(name="Foros creados", value=str(foros_creados), inline=True)
            embed.add_field(name="Hilos de curso creados", value=str(hilos_creados), inline=True)
            embed.add_field(name="Roles creados", value=str(roles_creados), inline=True)
            embed.add_field(name="Roles reutilizados", value=str(roles_reutilizados), inline=True)

            estado_orden = {True: "✅ verificada", False: "⚠️ revisar", None: "sin verificar"}[orden_roles]
            embed.add_field(
                name="Jerarquía de roles",
                value=_recortar(f"{roles_def[0]['nombre']} → … → {roles_def[-1]['nombre']} ({estado_orden})"),
                inline=False,
            )
            embed.add_field(
                name="Community",
                value=_recortar(f"✅ Activa — reglas: {canal_reglas.mention} · actualizaciones: {canal_updates.mention}"),
                inline=False,
            )

            if errores:
                texto_errores = "\n".join(f"• {e}" for e in errores[:10])
                if len(errores) > 10:
                    texto_errores += f"\n... y {len(errores) - 10} más"
                embed.add_field(name=f"⚠️ Avisos ({len(errores)})", value=_recortar(texto_errores), inline=False)

            if sobrantes:
                lista = ", ".join(sobrantes[:8]) + (f" y {len(sobrantes) - 8} más" if len(sobrantes) > 8 else "")
                embed.add_field(
                    name=f"ℹ️ Fuera de la estructura ({len(sobrantes)})",
                    value=_recortar(f"{lista}\nSon los que trae Discord por defecto; borralos a mano si no los querés."),
                    inline=False,
                )

            await aviso.edit(content=None, embed=embed)
        finally:
            self._en_curso.discard(guild.id)

    @server.error
    async def server_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("Este comando solo funciona dentro de un servidor.")
        elif isinstance(error, commands.CheckAnyFailure):
            await ctx.send(embed=embed_error("Necesitás permiso de Administrador o Gestionar Servidor para usar este comando."))
        else:
            await ctx.send(embed=embed_error(f"Ocurrió un error: {error}"))
            print(f"Error en !server: {error}")


async def setup(bot):
    await bot.add_cog(SetupServidorCog(bot))
