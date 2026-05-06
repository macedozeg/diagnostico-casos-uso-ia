import streamlit as st
import pandas as pd
from datetime import datetime

# ==============================
# CONFIG
# ==============================
st.set_page_config(
    page_title="Diagnóstico de Casos de Uso de IA",
    layout="wide"
)

ARCHIVO_CSV = "respuestas_diagnostico_ia.csv"

# ==============================
# ACTIVIDADES
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
        "Resolución de dudas sobre convocatorias"
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
    "Valoración de resultados y Transferencia": [
        "Planificación TRL",
        "Ofertas tecnológicas",
        "Búsqueda de socios",
        "Materiales de mercado",
        "Evaluación de resultados",
        "Planes de promoción",
        "Gestión del conocimiento"
    ],
    "Propiedad intelectual": [
        "Revisión de documentos de PI",
        "Estado del arte"
    ],
    "Comunicación": [
        "Contenidos web",
        "Memoria anual",
        "Newsletters",
        "Notas de prensa",
        "Correos",
        "Material gráfico",
        "Presentaciones",
        "Vídeos"
    ],
    "Recursos Humanos": [
        "Selección de perfiles",
        "Evaluación de candidaturas"
    ]
}

# ==============================
# TÍTULO
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
# IDENTIFICACIÓN
# ==============================
st.header("Identificación")

nombre = st.text_input("Nombre y apellidos *")
area = st.text_input("Área / Equipo")

if not nombre:
    st.warning("Introduce tu nombre para continuar")
    st.stop()

st.success("✅ Continúa con las actividades")
st.divider()

# ==============================
# SESSION STATE
# ==============================
if "actividades" not in st.session_state:
    st.session_state.actividades = []

def añadir():
    st.session_state.actividades.append({})

# BOTÓN INICIAL
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
        tiempo = st.selectbox("Consumo de tiempo", ["Bajo", "Medio", "Alto"], key=f"time{i}")

        beneficio = st.selectbox("¿Puede beneficiarse de IA?", ["No", "Sí"], key=f"bia{i}")

        uso = ""
        herramienta = ""
        licencia = ""
        coste = 0
        mejoras = ""
        implantacion = ""
        riesgos = []

        if beneficio == "Sí":

            uso = st.selectbox("Uso actual de IA", ["No", "Parcial", "Sí"], key=f"uso{i}")

            if uso in ["Parcial", "Sí"]:

                herramienta = st.text_input(
                    "IA principal utilizada",
                    placeholder="Ej: ChatGPT, Copilot",
                    key=f"herr{i}"
                )

                licencia = st.selectbox("Licencia", ["Gratis", "De Pago"], key=f"lic{i}")

                if licencia == "De Pago":
                    coste = st.number_input("Coste anual (€)", 0, step=50, key=f"cost{i}")

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
                key=f"ries{i}"
            )

        comentario = st.text_input("Comentario", key=f"com{i}")

        st.session_state.actividades[i] = {
            "Nombre": nombre,
            "Área": area,
            "Actividad general": ag,
            "Actividad específica": ae,
            "Repetitividad": rep,
            "Tiempo": tiempo,
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

# BOTÓN FINAL
if len(st.session_state.actividades) > 0:
    st.divider()
    st.button("➕ Añadir otra actividad", on_click=añadir)

# ==============================
# GUARDAR
# ==============================
st.divider()

if st.button("✅ Enviar respuestas"):

    if not st.session_state.actividades:
        st.warning("Añade al menos una actividad")
    else:
        df = pd.DataFrame(st.session_state.actividades)

        try:
            prev = pd.read_csv(ARCHIVO_CSV)
            df = pd.concat([prev, df])
        except:
            pass

        df.to_csv(ARCHIVO_CSV, index=False)

        st.success("✅ Respuestas guardadas correctamente")
        st.session_state.actividades = []
