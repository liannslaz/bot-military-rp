# -*- coding: utf-8 -*-
# Orden de arriba hacia abajo = jerarquía exacta pedida.
# "permisos_guild" son permisos de Discord a nivel servidor (no de canal).
# Todo lo que no sea Fundador/Administrador/Moderador/Supervisor RP va sin
# permisos administrativos de Discord — su acceso se maneja por canal.

ROLES = [
    # --- Administración del servidor ---
    {"nombre": "👑 | Fundador", "color": "#F59E0B",
     "permisos_guild": {"administrator": True}},
    {"nombre": "🛡️ | Administrador", "color": "#DC2626",
     "permisos_guild": {
         "manage_guild": True, "manage_channels": True, "manage_roles": True,
         "manage_messages": True, "manage_events": True, "kick_members": True,
         "ban_members": True, "moderate_members": True, "view_audit_log": True,
     }},
    {"nombre": "🔨 | Moderador", "color": "#2563EB",
     "permisos_guild": {
         "manage_messages": True, "kick_members": True, "moderate_members": True,
         "manage_threads": True, "view_audit_log": True,
     }},
    {"nombre": "📋 | Supervisor RP", "color": "#7C3AED",
     "permisos_guild": {"manage_messages": True, "manage_threads": True}},

    # --- Institucionales ---
    {"nombre": "🇲🇽 | Comandancia", "color": "#450A0A", "permisos_guild": {}},
    {"nombre": "📜 | Estado Mayor", "color": "#713F12", "permisos_guild": {}},
    {"nombre": "⚖️ | Justicia Militar", "color": "#312E81", "permisos_guild": {}},
    {"nombre": "🎖️ | Instructor", "color": "#78350F", "permisos_guild": {}},

    # --- Fuerzas Especiales ---
    {"nombre": "🏅 | Instructor de Fuerzas Especiales", "color": "#059669", "permisos_guild": {}},
    {"nombre": "🦅 | Comando", "color": "#047857", "permisos_guild": {}},
    {"nombre": "⚔️ | Operador de Fuerzas Especiales", "color": "#065F46", "permisos_guild": {}},
    {"nombre": "🟢 | Aspirante a Fuerzas Especiales", "color": "#064E3B", "permisos_guild": {}},

    # --- Alto mando (rangos) ---
    {"nombre": "🇲🇽 | General de División", "color": "#7F1D1D", "permisos_guild": {}},
    {"nombre": "⭐ | General de Brigada", "color": "#991B1B", "permisos_guild": {}},
    {"nombre": "🎖️ | General Brigadier", "color": "#B91C1C", "permisos_guild": {}},

    # --- Jefes ---
    {"nombre": "🏅 | Coronel", "color": "#9A3412", "permisos_guild": {}},
    {"nombre": "🎖️ | Teniente Coronel", "color": "#C2410C", "permisos_guild": {}},
    {"nombre": "🔰 | Mayor", "color": "#EA580C", "permisos_guild": {}},

    # --- Oficiales ---
    {"nombre": "⭐ | Capitán Primero", "color": "#B45309", "permisos_guild": {}},
    {"nombre": "⭐ | Capitán Segundo", "color": "#D97706", "permisos_guild": {}},
    {"nombre": "🔰 | Teniente", "color": "#CA8A04", "permisos_guild": {}},
    {"nombre": "🔰 | Subteniente", "color": "#A16207", "permisos_guild": {}},

    # --- Clases ---
    {"nombre": "🎗️ | Sargento Primero", "color": "#166534", "permisos_guild": {}},
    {"nombre": "🎗️ | Sargento Segundo", "color": "#15803D", "permisos_guild": {}},
    {"nombre": "🔹 | Cabo", "color": "#16A34A", "permisos_guild": {}},

    # --- Tropa ---
    {"nombre": "🪖 | Soldado", "color": "#374151", "permisos_guild": {}},
    {"nombre": "🎒 | Recluta", "color": "#4B5563", "permisos_guild": {}},

    # --- Cursos de especialización ---
    {"nombre": "🎯 | Tirador Selecto", "color": "#7C2D12", "permisos_guild": {}},
    {"nombre": "🛡️ | Seguridad Integral", "color": "#1E3A8A", "permisos_guild": {}},
    {"nombre": "🌊 | Buceo de Combate", "color": "#075985", "permisos_guild": {}},
    {"nombre": "⚠️ | Manejo de Explosivos", "color": "#92400E", "permisos_guild": {}},
    {"nombre": "🚤 | Operaciones Ribereñas", "color": "#0F766E", "permisos_guild": {}},
    {"nombre": "🛡️ | Contraterrorismo", "color": "#581C87", "permisos_guild": {}},

    # --- Apoyo y servicios ---
    {"nombre": "📡 | Comunicaciones", "color": "#4338CA", "permisos_guild": {}},
    {"nombre": "🏥 | Sanidad Militar", "color": "#BE123C", "permisos_guild": {}},
    {"nombre": "🚙 | Conductor Militar", "color": "#57534E", "permisos_guild": {}},
    {"nombre": "📻 | Operador de Radio", "color": "#4F46E5", "permisos_guild": {}},
    {"nombre": "📋 | Administración", "color": "#6B7280", "permisos_guild": {}},

    # --- Básico ---
    {"nombre": "👤 | Ciudadano", "color": "#6B7280", "permisos_guild": {}},
]

# Nombres de roles agrupados por función, usados para armar los permisos de canal.
ROL_FUNDADOR = "👑 | Fundador"
ROL_ADMINISTRADOR = "🛡️ | Administrador"
ROL_MODERADOR = "🔨 | Moderador"
ROL_SUPERVISOR_RP = "📋 | Supervisor RP"
ROL_COMANDANCIA = "🇲🇽 | Comandancia"
ROL_ESTADO_MAYOR = "📜 | Estado Mayor"
ROL_JUSTICIA_MILITAR = "⚖️ | Justicia Militar"
ROL_INSTRUCTOR = "🎖️ | Instructor"
ROL_INSTRUCTOR_FE = "🏅 | Instructor de Fuerzas Especiales"
ROL_CIUDADANO = "👤 | Ciudadano"

# "Staff" = quienes administran el servidor / moderan contenido
GRUPO_STAFF = [ROL_FUNDADOR, ROL_ADMINISTRADOR, ROL_MODERADOR, ROL_SUPERVISOR_RP]

# "Mando" = quienes dirigen la unidad a nivel narrativo
GRUPO_MANDO = [ROL_COMANDANCIA, ROL_ESTADO_MAYOR]

# "Instructores" = quienes gestionan formación/evaluaciones
GRUPO_INSTRUCTORES = [ROL_INSTRUCTOR, ROL_INSTRUCTOR_FE]

# "Personal militar" = todo lo que no es Staff puro ni Ciudadano (todos los
# rangos, fuerzas especiales, cursos y apoyo/servicios) — tiene acceso a las
# áreas internas de la unidad, a diferencia de un Ciudadano recién llegado.
GRUPO_PERSONAL_MILITAR = [
    r["nombre"] for r in ROLES
    if r["nombre"] not in GRUPO_STAFF + [ROL_CIUDADANO]
]
