import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================
# CONFIGURACIÓN GENERAL
# =====================================
st.set_page_config(
    page_title="Diagnóstico de Casos de Uso de IA",
    layout="wide"
)

ARCHIVO_CSV = "respuestas_diagnostico_ia.csv"

# =====================================
# CATÁLOGO DE ACTIVIDADES
# =====================================
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
        "Búsqueda de socios y networking",
        "Preparación de materiales orientados al mercado",
        "Evaluación de resultados",
        "Planes de promoción",
        "Gestión del conocimiento de los grupos"
    ],
    "Propiedad intelectual y patentabilidad": [
        "Revisión de documentos de PI",
        "Estado del arte de PI vinculada a la tecnología"
    ],
    "Comunicación y contenido": [
        "Contenidos web y redes sociales",
        "Memoria Anual",
        "Newsletters",
        "Notas de Prensa",
        "Correos de difusión",
        "Materiales gráficos y comerciales",
        "Presentaciones",
        "Vídeos"
    ],
    "Recursos Humanos": [
        "Identificación del perfil a contratar",
        "Evaluación de candidaturas"
    ]
}

# =====================================
# TÍTULO
# =====================================
st.title("Diagnóstico operativo de Casos de Uso de IA")

st.write(
    "Este cuestionario permite identificar actividades susceptibles de "
    "mejora mediante tecnologías de automatización e inteligencia artificial." 
    " Primero indícanos tus datos, luego añade todas las actividades (dando click en añadir actividad) que consideres susceptibles del uso de IA." 
    " Al añadir una actividad, primero selecciona la actividad general y según ello elige la actividad específica asociada."
    " Finalmente, luego de añadir todas las actividades que creas conveniente, da click en Enviar respuestas."
    " En caso de dudas, escribe a Miguel Macedo a macedoma@unican.es."
)

# =====================================
# IDENTIFICACIÓN
# =====================================
st.header("Identificación del respondiente")

nombre = st.text_input("Nombre y apellidos *")
area = st.text_input("Área / Equipo")

if not nombre:
    st.warning("Por favor, indica tu nombre.")
    st.stop()

st.success("Identificación completada 👇")
st.divider()

# =====================================
# ESTADO
# =====================================
if "actividades" not in st.session_state:
    st.session_state.actividades = []

def añadir():
    st.session_state.actividades.append({})

# Botón inicial
if len(st.session_state.actividades) == 0:
    st.button("➕ Añadir actividad", on_click=añadir)

# =====================================
# FORMULARIO
# =====================================
for i in range(len(st.session_state.actividades)):

    with st.container(border=True):

        st.subheader(f"Actividad {i+1}")

        ag = st.selectbox(
            "Actividad general",
            list(ACTIVIDADES.keys()),
            key=f"ag_{i}"
        )

        ae = st.selectbox(
            "Actividad específica",
            ACTIVIDADES[ag],
            key=f"ae_{i}"
        )

        rep = st.selectbox(
            "Repetitividad",
            ["Bajo", "Medio", "Alto"],
            key=f"rep_{i}"
        )

        tiempo = st.selectbox(
            "Consumo de tiempo",
            ["Bajo", "Medio", "Alto"],
            key=f"time_{i}"
        )

        beneficio = st.selectbox(
            "¿Puede beneficiarse de IA?",
            ["No", "Sí"],
            key=f"bia_{i}"
        )

        uso = ""
        herramienta = ""
        licencia = ""
        coste = 0
        mejoras = ""
        plazo = ""
        riesgos = []

        if beneficio == "Sí":

            uso = st.selectbox(
                "Uso actual de IA",
                ["No", "Parcial", "Sí"],
                key=f"uso_{i}"
            )

            if uso in ["Parcial", "Sí"]:

                herramienta = st.text_input(
                    "IA principal utilizada",
                    placeholder="Ej: ChatGPT, Copilot",
                    key=f"herr_{i}"
                )

                licencia = st.selectbox(
                    "Licencia",
                    ["Gratis", "De Pago"],
                    key=f"lic_{i}"
                )

                if licencia == "De Pago":
                    coste = st.number_input(
                        "Coste anual (€)",
                        min_value=0,
                        step=50,
                        key=f"cost_{i}"
                    )

            mejoras = st.text_area(
                "Mejoras esperadas con IA",
                key=f"mej_{i}"
            )

            plazo = st.selectbox(
                "Plazo",
                [
                    "Corto Plazo: impacto inmediato",
                    "Mediano Plazo: requiere preparación",
                    "Largo Plazo: cambio estructural"
                ],
                key=f"plazo_{i}"
            )

            riesgos = st.multiselect(
                "Riesgos",
                [
                    "Privacidad",
                    "Calidad",
                    "Control",
                    "Presupuesto",
                    "Otro"
                ],
                key=f"riesgos_{i}"
            )

        comentario = st.text_input(
            "Comentario",
            key=f"com_{i}"
        )

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
            "Plazo": plazo,
            "Riesgos": "; ".join(riesgos),
            "Comentario": comentario,
            "Fecha": datetime.now().isoformat()
        }

# Botón final
if len(st.session_state.actividades) > 0:
    st.divider()
    st.button("➕ Añadir otra actividad", on_click=añadir)

# =====================================
# GUARDAR
# =====================================
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

        st.success("✅ Respuestas guardadas")
        st.session_state.actividades = []
