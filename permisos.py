# -*- coding: utf-8 -*-
import discord

from roles_data import (
    ROL_FUNDADOR, ROL_ADMINISTRADOR, ROL_MODERADOR, ROL_SUPERVISOR_RP,
    ROL_COMANDANCIA, ROL_ESTADO_MAYOR, ROL_JUSTICIA_MILITAR,
    ROL_INSTRUCTOR, ROL_INSTRUCTOR_FE, ROL_CIUDADANO,
    GRUPO_STAFF, GRUPO_MANDO, GRUPO_INSTRUCTORES, GRUPO_PERSONAL_MILITAR,
)

# ---------- Niveles de permiso reutilizables ----------
def _ver_solo_lectura():
    return discord.PermissionOverwrite(view_channel=True, read_message_history=True, send_messages=False)


def _ver():
    return discord.PermissionOverwrite(view_channel=True, read_message_history=True)


def _ver_escribir():
    return discord.PermissionOverwrite(
        view_channel=True, read_message_history=True, send_messages=True,
        connect=True, speak=True
    )


def _gestionar():
    return discord.PermissionOverwrite(
        view_channel=True, read_message_history=True, send_messages=True,
        manage_messages=True, manage_threads=True, connect=True, speak=True
    )


def _sin_acceso():
    return discord.PermissionOverwrite(view_channel=False, connect=False)


def _conectar_hablar():
    return discord.PermissionOverwrite(view_channel=True, connect=True, speak=True)


def _voz_moderar():
    return discord.PermissionOverwrite(
        view_channel=True, connect=True, speak=True,
        mute_members=True, deafen_members=True, move_members=True
    )


# ---------- Overwrites por categoría (clave = "acceso" en estructura.py) ----------
def overwrites_categoria(acceso: str, guild):
    everyone = guild.default_role

    def roles(nombres):
        objs = [discord.utils.get(guild.roles, name=n) for n in nombres]
        return [r for r in objs if r is not None]

    base = {}

    if acceso == "verificacion":
        base[everyone] = _ver_solo_lectura()
        for r in roles(GRUPO_STAFF):
            base[r] = _gestionar()

    elif acceso in ("informacion", "chat", "soporte", "reconocimientos"):
        base[everyone] = _ver_escribir() if acceso in ("chat", "soporte") else _ver()
        for r in roles(GRUPO_STAFF):
            base[r] = _gestionar()

    elif acceso == "unidad":
        base[everyone] = _sin_acceso()
        base[discord.utils.get(guild.roles, name=ROL_CIUDADANO)] = _ver()
        for r in roles(GRUPO_PERSONAL_MILITAR):
            base[r] = _ver_escribir()
        for r in roles(GRUPO_MANDO + GRUPO_STAFF):
            base[r] = _gestionar()

    elif acceso == "reclutamiento":
        base[everyone] = _ver()
        for r in roles(GRUPO_STAFF + GRUPO_MANDO):
            base[r] = _gestionar()

    elif acceso == "jerarquia":
        base[everyone] = _sin_acceso()
        base[discord.utils.get(guild.roles, name=ROL_CIUDADANO)] = _ver()
        for r in roles(GRUPO_PERSONAL_MILITAR):
            base[r] = _ver()
        for r in roles(GRUPO_MANDO + GRUPO_STAFF):
            base[r] = _gestionar()

    elif acceso == "personal":
        base[everyone] = _sin_acceso()
        for r in roles(GRUPO_PERSONAL_MILITAR):
            base[r] = _ver()
        for r in roles(GRUPO_MANDO + GRUPO_STAFF):
            base[r] = _gestionar()

    elif acceso == "formacion":
        base[everyone] = _sin_acceso()
        for r in roles(GRUPO_PERSONAL_MILITAR):
            base[r] = _ver_escribir()
        for r in roles(GRUPO_INSTRUCTORES + GRUPO_MANDO + GRUPO_STAFF):
            base[r] = _gestionar()

    elif acceso == "operaciones":
        base[everyone] = _sin_acceso()
        for r in roles(GRUPO_PERSONAL_MILITAR):
            base[r] = _ver_escribir()
        for r in roles(GRUPO_MANDO + GRUPO_STAFF):
            base[r] = _gestionar()

    elif acceso == "planificacion":
        base[everyone] = _sin_acceso()
        for r in roles(GRUPO_PERSONAL_MILITAR):
            base[r] = _ver()
        for r in roles(GRUPO_MANDO + GRUPO_STAFF):
            base[r] = _gestionar()

    elif acceso == "reportes":
        base[everyone] = _ver_escribir()
        rol_supervisor = discord.utils.get(guild.roles, name=ROL_SUPERVISOR_RP)
        rol_moderador = discord.utils.get(guild.roles, name=ROL_MODERADOR)
        rol_justicia = discord.utils.get(guild.roles, name=ROL_JUSTICIA_MILITAR)
        for r in [x for x in [rol_supervisor, rol_moderador, rol_justicia] if x]:
            base[r] = _gestionar()
        for r in roles(GRUPO_MANDO + [ROL_FUNDADOR, ROL_ADMINISTRADOR]):
            base[r] = _gestionar()

    elif acceso == "archivo":
        base[everyone] = _sin_acceso()
        rol_ciudadano = discord.utils.get(guild.roles, name=ROL_CIUDADANO)
        if rol_ciudadano:
            base[rol_ciudadano] = _sin_acceso()
        for r in roles(GRUPO_PERSONAL_MILITAR):
            base[r] = _ver()
        for r in roles(GRUPO_MANDO + GRUPO_STAFF):
            base[r] = _gestionar()

    elif acceso == "comunicaciones":
        base[everyone] = _sin_acceso()
        rol_ciudadano = discord.utils.get(guild.roles, name=ROL_CIUDADANO)
        if rol_ciudadano:
            base[rol_ciudadano] = _sin_acceso()
        for r in roles(GRUPO_PERSONAL_MILITAR):
            base[r] = _conectar_hablar()
        for r in roles(GRUPO_MANDO + GRUPO_STAFF):
            base[r] = _voz_moderar()

    elif acceso == "mando":
        base[everyone] = _sin_acceso()
        rol_ciudadano = discord.utils.get(guild.roles, name=ROL_CIUDADANO)
        if rol_ciudadano:
            base[rol_ciudadano] = _sin_acceso()
        for r in roles(GRUPO_PERSONAL_MILITAR):
            base[r] = _ver()
        for r in roles(GRUPO_MANDO):
            base[r] = _gestionar()
        for r in roles(GRUPO_STAFF):
            base[r] = _gestionar()

    return {k: v for k, v in base.items() if k is not None}


# ---------- Overwrites específicos por canal (sobreescriben lo de la categoría) ----------
def overwrites_canal_especifico(clave: str, guild):
    everyone = guild.default_role

    def roles(nombres):
        objs = [discord.utils.get(guild.roles, name=n) for n in nombres]
        return [r for r in objs if r is not None]

    if clave == "solo_moderacion":
        # 「🔒」Moderador: SOLO Moderador, Administrador y Fundador
        base = {everyone: _sin_acceso()}
        for r in roles([ROL_MODERADOR, ROL_ADMINISTRADOR, ROL_FUNDADOR]):
            base[r] = _gestionar()
        return base

    if clave == "reclutamiento_admisiones":
        # Solo personal autorizado gestiona admisiones (los demás no ven este canal puntual)
        base = {everyone: _sin_acceso()}
        for r in roles(GRUPO_MANDO + GRUPO_STAFF):
            base[r] = _gestionar()
        return base

    if clave == "reportes_archivo":
        # Reportes internos: solo Mando/Justicia Militar/Staff (no todos los miembros)
        base = {everyone: _sin_acceso()}
        for r in roles(GRUPO_MANDO + GRUPO_STAFF + [ROL_JUSTICIA_MILITAR]):
            base[r] = _gestionar()
        return base

    if clave == "comunicaciones_mando":
        base = {everyone: _sin_acceso()}
        for r in roles(GRUPO_MANDO + GRUPO_STAFF):
            base[r] = _voz_moderar()
        return base

    if clave == "abierto_todos":
        return {everyone: _conectar_hablar()}

    return None
