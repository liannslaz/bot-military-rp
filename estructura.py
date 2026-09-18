# -*- coding: utf-8 -*-
from ids_existentes import CANAL_REGLAS_ID, CANAL_MODERADOR_ID

# tipo: "texto" | "voz" | "foro"
# id_existente: si se da, se busca primero por ese ID antes que por nombre.

TAGS_FORO = ["Información", "Material", "Evaluación", "Resultados"]
HILOS_FORO = ["📖 Información", "📚 Material", "📝 Evaluación", "🏅 Resultados"]

FOROS_FORMACION = [
    "「🎯」𝙲𝚞𝚛𝚜𝚘-𝚍𝚎-𝙾𝚙𝚎𝚛𝚊𝚌𝚒𝚘𝚗𝚎𝚜-𝚃𝚊́𝚌𝚝𝚒𝚌𝚊𝚜-𝚍𝚎-𝙲𝚘𝚗𝚝𝚛𝚊𝚝𝚎𝚛𝚛𝚘𝚛𝚒𝚜𝚖𝚘",
    "「🎯」𝙲𝚞𝚛𝚜𝚘-𝚍𝚎-𝚃𝚒𝚛𝚊𝚍𝚘𝚛-𝚂𝚎𝚕𝚎𝚌𝚝𝚘",
    "「🛡️」𝙲𝚞𝚛𝚜𝚘-𝚍𝚎-𝚂𝚎𝚐𝚞𝚛𝚒𝚍𝚊𝚍-𝙸𝚗𝚝𝚎𝚐𝚛𝚊𝚕",
    "「🌊」𝙲𝚞𝚛𝚜𝚘-𝚍𝚎-𝙱𝚞𝚌𝚎𝚘-𝚍𝚎-𝙲𝚘𝚖𝚋𝚊𝚝𝚎",
    "「💣」𝙲𝚞𝚛𝚜𝚘-𝚍𝚎-𝙼𝚊𝚗𝚎𝚓𝚘-𝚍𝚎-𝙴𝚡𝚙𝚕𝚘𝚜𝚒𝚟𝚘𝚜",
    "「🚤」𝙲𝚞𝚛𝚜𝚘-𝚍𝚎-𝙾𝚙𝚎𝚛𝚊𝚌𝚒𝚘𝚗𝚎𝚜-𝚁𝚒𝚋𝚎𝚛𝚎𝚗̃𝚊𝚜",
]

ESTRUCTURA = [
    {
        "nombre": "❘ ═════ | 𝗩𝗘𝗥𝗜𝗙𝗜𝗖𝗔𝗖𝗜𝗢́𝗡 | ═════ ❘",
        "acceso": "verificacion",
        "canales": [
            {"nombre": "「📜」𝚁𝚎𝚐𝚕𝚊𝚜", "tipo": "texto", "id_existente": CANAL_REGLAS_ID},
            {"nombre": "「📌」𝙸𝚗𝚏𝚘𝚛𝚖𝚊𝚌𝚒𝚘́𝚗", "tipo": "texto"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗖𝗜𝗢́𝗡 | ═════ ❘",
        "acceso": "informacion",
        "canales": [
            {"nombre": "「📢」𝙰𝚗𝚞𝚗𝚌𝚒𝚘𝚜", "tipo": "texto"},
            {"nombre": "「📝」𝙻𝚒𝚗𝚎𝚊-𝙾𝚏𝚒𝚌𝚒𝚊𝚕", "tipo": "texto"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗔𝗚𝗘𝗡𝗗𝗔 | ═════ ❘",
        "acceso": "informacion",
        "canales": [
            {"nombre": "「📅」𝙰𝚐𝚎𝚗𝚍𝚊-𝚂𝚎𝚖𝚊𝚗𝚊𝚕", "tipo": "texto"},
            {"nombre": "「📆」𝙲𝚊𝚕𝚎𝚗𝚍𝚊𝚛𝚒𝚘", "tipo": "texto"},
            {"nombre": "「📍」𝙰𝚌𝚝𝚒𝚟𝚒𝚍𝚊𝚍𝚎𝚜", "tipo": "texto"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗖𝗛𝗔𝗧 | ═════ ❘",
        "acceso": "chat",
        "canales": [
            {"nombre": "「💬」𝙲𝚑𝚊𝚝-𝙶𝚎𝚗𝚎𝚛𝚊𝚕", "tipo": "texto"},
            {"nombre": "「📸」𝙼𝚞𝚕𝚝𝚒𝚖𝚎𝚍𝚒𝚊", "tipo": "texto"},
            {"nombre": "「💡」𝚂𝚞𝚐𝚎𝚛𝚎𝚗𝚌𝚒𝚊𝚜", "tipo": "texto"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗦𝗢𝗣𝗢𝗥𝗧𝗘 | ═════ ❘",
        "acceso": "soporte",
        "canales": [
            {"nombre": "「🎫」𝚂𝚘𝚙𝚘𝚛𝚝𝚎", "tipo": "texto"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗨𝗡𝗜𝗗𝗔𝗗 | ═════ ❘",
        "acceso": "unidad",
        "canales": [
            {"nombre": "「🎖️」𝙸𝚗𝚏𝚘𝚛𝚖𝚊𝚌𝚒𝚘́𝚗-𝚍𝚎-𝚕𝚊-𝚄𝚗𝚒𝚍𝚊𝚍", "tipo": "texto"},
            {"nombre": "「👥」𝙿𝚎𝚛𝚜𝚘𝚗𝚊𝚕", "tipo": "texto"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗥𝗘𝗖𝗟𝗨𝗧𝗔𝗠𝗜𝗘𝗡𝗧𝗢 | ═════ ❘",
        "acceso": "reclutamiento",
        "canales": [
            {"nombre": "「📋」𝙸𝚗𝚜𝚌𝚛𝚒𝚙𝚌𝚒𝚘𝚗𝚎𝚜", "tipo": "texto"},
            {"nombre": "「📑」𝚁𝚎𝚚𝚞𝚒𝚜𝚒𝚝𝚘𝚜", "tipo": "texto"},
            {"nombre": "「🎖️」𝙰𝚍𝚖𝚒𝚜𝚒𝚘𝚗𝚎𝚜", "tipo": "texto", "acceso_canal": "reclutamiento_admisiones"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗝𝗘𝗥𝗔𝗥𝗤𝗨𝗜́𝗔 | ═════ ❘",
        "acceso": "jerarquia",
        "canales": [
            {"nombre": "「🎖️」𝙶𝚛𝚊𝚍𝚘𝚜-𝚢-𝙹𝚎𝚛𝚊𝚛𝚚𝚞𝚒́𝚊", "tipo": "texto"},
            {"nombre": "「👤」𝙼𝚊𝚗𝚍𝚘-𝚍𝚎-𝚕𝚊-𝚄𝚗𝚒𝚍𝚊𝚍", "tipo": "texto"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗣𝗘𝗥𝗦𝗢𝗡𝗔𝗟 | ═════ ❘",
        "acceso": "personal",
        "canales": [
            {"nombre": "「📋」𝙵𝚒𝚌𝚑𝚊𝚜", "tipo": "texto"},
            {"nombre": "「📈」𝙰𝚜𝚌𝚎𝚗𝚜𝚘𝚜", "tipo": "texto"},
            {"nombre": "「🏅」𝙲𝚘𝚗𝚍𝚎𝚌𝚘𝚛𝚊𝚌𝚒𝚘𝚗𝚎𝚜", "tipo": "texto"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗙𝗢𝗥𝗠𝗔𝗖𝗜𝗢́𝗡 | ═════ ❘",
        "acceso": "formacion",
        "canales": [{"nombre": nombre, "tipo": "foro"} for nombre in FOROS_FORMACION],
    },
    {
        "nombre": "❘ ═════ | 𝗘𝗩𝗔𝗟𝗨𝗔𝗖𝗜𝗢́𝗡 | ═════ ❘",
        "acceso": "formacion",
        "canales": [
            {"nombre": "「📚」𝙼𝚊𝚝𝚎𝚛𝚒𝚊𝚕", "tipo": "texto"},
            {"nombre": "「📝」𝙴𝚟𝚊𝚕𝚞𝚊𝚌𝚒𝚘𝚗𝚎𝚜", "tipo": "texto"},
            {"nombre": "「🏆」𝚁𝚎𝚜𝚞𝚕𝚝𝚊𝚍𝚘𝚜", "tipo": "texto"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗢𝗣𝗘𝗥𝗔𝗖𝗜𝗢𝗡𝗘𝗦 | ═════ ❘",
        "acceso": "operaciones",
        "canales": [
            {"nombre": "「🎯」𝙼𝚒𝚜𝚒𝚘𝚗𝚎𝚜", "tipo": "texto"},
            {"nombre": "「🗃️」𝙰𝚛𝚌𝚑𝚒𝚟𝚘-𝚍𝚎-𝙼𝚒𝚜𝚒𝚘𝚗𝚎𝚜", "tipo": "texto"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗣𝗟𝗔𝗡𝗜𝗙𝗜𝗖𝗔𝗖𝗜𝗢́𝗡 | ═════ ❘",
        "acceso": "planificacion",
        "canales": [
            {"nombre": "「📋」𝙿𝚕𝚊𝚗𝚒𝚏𝚒𝚌𝚊𝚌𝚒𝚘́𝚗", "tipo": "texto"},
            {"nombre": "「📡」𝙱𝚛𝚒𝚎𝚏𝚒𝚗𝚐", "tipo": "texto"},
            {"nombre": "「📄」𝙸𝚗𝚏𝚘𝚛𝚖𝚎𝚜", "tipo": "texto"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗥𝗘𝗣𝗢𝗥𝗧𝗘𝗦 | ═════ ❘",
        "acceso": "reportes",
        "canales": [
            {"nombre": "「📝」𝚁𝚎𝚙𝚘𝚛𝚝𝚎𝚜", "tipo": "texto"},
            {"nombre": "「📋」𝙸𝚗𝚌𝚒𝚍𝚎𝚗𝚌𝚒𝚊𝚜", "tipo": "texto"},
            {"nombre": "「📁」𝙰𝚛𝚌𝚑𝚒𝚟𝚘-𝚍𝚎-𝚁𝚎𝚙𝚘𝚛𝚝𝚎𝚜", "tipo": "texto", "acceso_canal": "reportes_archivo"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗥𝗘𝗖𝗢𝗡𝗢𝗖𝗜𝗠𝗜𝗘𝗡𝗧𝗢𝗦 | ═════ ❘",
        "acceso": "reconocimientos",
        "canales": [
            {"nombre": "「🏆」𝙼𝚎𝚛𝚒𝚝𝚘𝚜", "tipo": "texto"},
            {"nombre": "「🎖️」𝙲𝚘𝚗𝚍𝚎𝚌𝚘𝚛𝚊𝚌𝚒𝚘𝚗𝚎𝚜", "tipo": "texto"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗔𝗥𝗖𝗛𝗜𝗩𝗢 | ═════ ❘",
        "acceso": "archivo",
        "canales": [
            {"nombre": "「📂」𝙰𝚛𝚌𝚑𝚒𝚟𝚘-𝙶𝚎𝚗𝚎𝚛𝚊𝚕", "tipo": "texto"},
            {"nombre": "「📜」𝙷𝚒𝚜𝚝𝚘𝚛𝚒𝚊-𝚍𝚎-𝚕𝚊-𝚄𝚗𝚒𝚍𝚊𝚍", "tipo": "texto"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗖𝗢𝗠𝗨𝗡𝗜𝗖𝗔𝗖𝗜𝗢𝗡𝗘𝗦 | ═════ ❘",
        "acceso": "comunicaciones",
        "canales": [
            {"nombre": "🔊・𝙶𝚎𝚗𝚎𝚛𝚊𝚕", "tipo": "voz"},
            {"nombre": "🔊・𝙲𝚘𝚖𝚊𝚗𝚍𝚘", "tipo": "voz", "acceso_canal": "comunicaciones_mando"},
            {"nombre": "🔊・𝙱𝚛𝚒𝚎𝚏𝚒𝚗𝚐", "tipo": "voz"},
            {"nombre": "🔊・𝙼𝚒𝚜𝚒𝚘𝚗𝚎𝚜", "tipo": "voz"},
            {"nombre": "🔊・𝙴𝚗𝚝𝚛𝚎𝚗𝚊𝚖𝚒𝚎𝚗𝚝𝚘", "tipo": "voz"},
            {"nombre": "🔊・𝙰𝙵𝙺", "tipo": "voz", "acceso_canal": "abierto_todos"},
        ],
    },
    {
        "nombre": "❘ ═════ | 𝗠𝗔𝗡𝗗𝗢 | ═════ ❘",
        "acceso": "mando",
        "canales": [
            {"nombre": "「🎖️」𝙾́𝚛𝚍𝚎𝚗𝚎𝚜", "tipo": "texto"},
            {"nombre": "「📑」𝙸𝚗𝚏𝚘𝚛𝚖𝚎𝚜-𝙸𝚗𝚝𝚎𝚛𝚗𝚘𝚜", "tipo": "texto"},
            {"nombre": "「🗂️」𝙰𝚛𝚌𝚑𝚒𝚟𝚘", "tipo": "texto"},
            {"nombre": "「🔒」𝙼𝚘𝚍𝚎𝚛𝚊𝚍𝚘𝚛", "tipo": "texto", "id_existente": CANAL_MODERADOR_ID,
             "acceso_canal": "solo_moderacion"},
        ],
    },
]
