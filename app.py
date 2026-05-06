import streamlit as st
from datetime import datetime
import requests

# ==============================
# CONFIGURACIÓN
# ==============================

URL_API = "https://script.google.com/macros/s/AKfycbweMR8oum94CxPh2jVERaSgoOhX8iieHuDoB-IM1GDQHBVtct6RMS9OgDoKD9HwaqA/exec"

st.set_page_config(page_title="Diagnóstico IA", layout="wide")

# ==============================
# ESTADO
# ==============================

if "actividades" not in st.session_state:
    st.session_state.actividades = []

if "enviado" not in st.session_state:
    st.session_state.enviado = False

# ==============================
# CATÁLOGO COMPLETO (TUYO)
# ==============================

ACTIVIDADES = {
    "Procesos administrativos internos": [
        "Gestión de correos electrónicos",
        "Transcripción y resumen de reuniones o entrevistas",
        "Gestión y actualización de bases de datos (Excel)",
        "Gestión y planificación interna de equipos",
        "Recordatorios",
        "Hojas de pedidos para gastos",
        "Justificaciones de gastos",
        "Archivo y recuperación de documentación",
        "Resúmenes de asistencia a viajes o ferias",
        "Envío masivo de emails personalizados",
        "Elaboración de informes de actividad"
    ],
    "Convocatorias y Licitaciones": [
        "Revisión y resumen de Bases: Convocatorias y Licitaciones",
        "Preparación administrativa de propuestas/proyectos",
        "Búsqueda de información (general / investigación / mercado)",
        "Resolución de dudas sobre convocatorias, considerando FAQs"
    ],
    "Preparación de propuestas y proyectos": [
        "Elaboración de memoria técnico-económica",
        "Scouting y detección de resultados de investigación"
    ],
    "Gestión contractual y legal": [
        "Revisión y negociación de acuerdos",
        "Comparación de versiones de acuerdos",
        "Búsqueda de marco legislativo"
    ],
    "Valoración de resultados de investigación y Transferencia tecnológica comercial": [
        "Planificación y seguimiento de actividades (TRL)",
        "Elaboración de Ofertas Tecnológicas",
        "Búsqueda de socios, networking, identificación de contactos",
        "Preparación de presentaciones y materiales de difusión (orientadas al mercado)",
        "Evaluación de resultados",
        "Planes de promoción de los resultados de investigación",
        "Gestión del conocimiento de los grupos de investigación"
    ],
    "Propiedad intelectual y patentabilidad": [
        "Revisión de documentos vinculados a Derechos de Propiedad Intelectual",
        "Estado del arte de Derechos de Propiedad Intelectual vinculada a la tecnología de trabajo o desarrollo"
    ],
    "Comunicación y contenido": [
        "Elaboración y actualización de contenidos web y redes sociales",
        "Elaboración, revisión, publicación y actualización de Memoria Anual",
        "Elaboración, revisión, publicación y actualización de Newsletters",
        "Elaboración, revisión, publicación de Notas de Prensa",
        "Redacción de correos de difusión",
        "Generación de materiales gráficos y comerciales",
        "Preparación de presentaciones",
        "Preparación de vídeos"
    ],
    "Recursos Humanos": [
        "Identificación o selección del perfil a contratar",
        "Evaluación de proyectos y candidaturas"
    ]
}

# ==============================
# INTERFAZ
# ==============================

st.title("Diagnóstico de Casos de Uso de IA")

st.markdown("""
**Instrucciones:**

1) Este cuestionario permite identificar actividades susceptibles de mejora mediante tecnologías de automatización e inteligencia artificial.
2) Primero indícanos tus datos, luego añade todas las actividades que consideres susceptibles del uso de IA (has click en añadir actividad) .
3) Al añadir una actividad, primero selecciona la actividad general y según ello elige la actividad específica asociada. Completa la información solicitada.
4) Finalmente, luego de añadir todas las actividades que creas conveniente, haz click en Enviar respuestas.

📩 Dudas: macedoma@unican.es
""")

# ==============================
# BLOQUEO SI YA ENVIADO
# ==============================

if st.session_state.enviado:
    st.success("✅ Gracias, el formulario ha sido enviado correctamente.")

    if st.button("🔄 Enviar otro formulario"):
        st.session_state.enviado = False
        st.session_state.actividades = []

    st.stop()

# ==============================
# IDENTIFICACIÓN
# ==============================

nombre = st.text_input("Nombre *")
area = st.text_input("Área / Equipo")

if not nombre:
    st.warning("Introduce tu nombre para continuar")
    st.stop()

# ==============================
# FUNCIONES
# ==============================

def añadir():
    st.session_state.actividades.append({})

# ==============================
# BOTÓN INICIAL
# ==============================

if len(st.session_state.actividades) == 0:
    st.button("➕ Añadir actividad", on_click=añadir)

# ==============================
# FORMULARIO
# ==============================

for i in range(len(st.session_state.actividades)):

    with st.container(border=True):

        st.subheader(f"Actividad {i+1}")

        ag = st.selectbox("Actividad general", list(ACTIVIDADES.keys()), key=f"ag{i}")
        ae = st.selectbox("Actividad específica", ACTIVIDADES[ag], key=f"ae{i}")

        rep = st.selectbox("Repetitividad", ["Bajo", "Medio", "Alto"], key=f"rep{i}")
        tiempo = st.selectbox("Tiempo", ["Bajo", "Medio", "Alto"], key=f"time{i}")

        equipo = st.selectbox(
            "¿Participan varias personas del equipo?",
            ["No", "Sí"],
            key=f"equipo{i}"
        )

        beneficio = st.selectbox(
            "¿Puede beneficiarse de IA?",
            ["No", "Sí"],
            key=f"bia{i}"
        )

        uso = ""
        herramienta = ""
        licencia = ""
        coste = 0
        mejoras = ""
        implantacion = ""
        riesgos = []

        if beneficio == "Sí":

            uso = st.selectbox("Uso de IA", ["No", "Parcial", "Sí"], key=f"uso{i}")

            if uso in ["Parcial", "Sí"]:
                herramienta = st.text_input("IA principal utilizada", key=f"herr{i}")
                licencia = st.selectbox("Licencia", ["Gratis", "De Pago"], key=f"lic{i}")

                if licencia == "De Pago":
                    coste = st.number_input("Coste anual (€)", 0, key=f"cost{i}")

            mejoras = st.text_area("Mejoras esperadas con IA", key=f"mej{i}")

            implantacion = st.selectbox(
                "Nivel de implantación",
                [
                    "Corto plazo: impacto inmediato",
                    "Medio plazo: requiere preparación",
                    "Largo plazo: cambio estructural"
                ],
                key=f"impl{i}"
            )

            riesgos = st.multiselect(
                "Riesgos",
                ["Privacidad", "Calidad", "Control", "Presupuesto", "Otro"],
                key=f"riesgos{i}"
            )

        comentario = st.text_input("Comentario", key=f"com{i}")

        st.session_state.actividades[i] = {
            "Nombre": nombre,
            "Área": area,
            "Actividad general": ag,
            "Actividad específica": ae,
            "Repetitividad": rep,
            "Tiempo": tiempo,
            "Participación equipo": equipo,
            "Beneficio IA": beneficio,
            "Uso IA": uso,
            "IA principal": herramienta,
            "Licencia": licencia,
            "Coste": coste,
            "Mejoras": mejoras,
            "Implantación": implantacion,
            "Riesgos": "; ".join(riesgos),
            "Comentario": comentario,
            "Fecha": datetime.now().isoformat()
        }

# ==============================
# BOTÓN FINAL
# ==============================

if len(st.session_state.actividades) > 0:
    st.button("➕ Añadir otra actividad", on_click=añadir)

# ==============================
# ENVÍO
# ==============================

if st.button("✅ Enviar respuestas"):

    if not st.session_state.actividades:
        st.warning("Añade al menos una actividad")
    else:
        try:
            for fila in st.session_state.actividades:
                requests.post(URL_API, json=fila)

            st.session_state.actividades = []
            st.session_state.enviado = True
            st.rerun()

        except Exception as e:
            st.error(f"Error al enviar datos: {e}")
