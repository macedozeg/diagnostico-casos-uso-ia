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
)

# =====================================
# IDENTIFICACIÓN DEL RESPONDIENTE (SE MANTIENE)
# =====================================
st.header("Identificación del respondiente")

nombre = st.text_input("Nombre y apellidos *")
area = st.text_input("Área / Equipo")

if not nombre:
    st.warning("Por favor, indica tu nombre para continuar.")
    st.stop()

st.success("Identificación completada. Continúa con el cuestionario 👇")
st.divider()

# =====================================
# ESTADO DE ACTIVIDADES
# =====================================
if "actividades" not in st.session_state:
    st.session_state.actividades = []

def añadir_actividad():
    st.session_state.actividades.append({})

st.button("➕ Añadir actividad", on_click=añadir_actividad)

# =====================================
# FORMULARIO POR ACTIVIDAD
# =====================================
for idx in range(len(st.session_state.actividades)):

    with st.container(border=True):

        st.subheader(f"Actividad {idx + 1}")

        actividad_general = st.selectbox(
            "Actividad general",
            list(ACTIVIDADES.keys()),
            key=f"ag_{idx}"
        )

        actividad_especifica = st.selectbox(
            "Actividad específica",
            ACTIVIDADES[actividad_general],
            key=f"ae_{idx}"
        )

        repetitividad = st.selectbox(
            "¿Es una actividad repetitiva?",
            ["Bajo", "Medio", "Alto"],
            key=f"rep_{idx}"
        )

        tiempo = st.selectbox(
            "¿Consume mucho tiempo?",
            ["Bajo", "Medio", "Alto"],
            key=f"time_{idx}"
        )

        beneficio_ia = st.selectbox(
            "¿Esta actividad se puede beneficiar del aporte de IA?",
            ["No", "Sí"],
            key=f"bia_{idx}"
        )

        uso_ia = ""
        nombre_ia = ""
        plazo = ""
        riesgos = []

        if beneficio_ia == "Sí":

            uso_ia = st.selectbox(
                "¿Atiende parte de esta actividad con IA?",
                ["No", "Parcial", "Sí"],
                key=f"uia_{idx}"
            )

            if uso_ia in ["Parcial", "Sí"]:
                nombre_ia = st.text_input(
                    "Nombre de la(s) IA(s)",
                    placeholder="Ej: ChatGPT; Copilot",
                    key=f"nia_{idx}"
                )

            plazo = st.selectbox(
                "Plazo de implantación",
                [
                    "Corto Plazo: Con impacto inmediato",
                    "Mediano Plazo: Se requiere la preparación del equipo",
                    "Largo Plazo: Se atenderá objetivos estructurales del equipo o de IH"
                ],
                key=f"plazo_{idx}"
            )

            riesgos = st.multiselect(
                "Riesgos percibidos asociados a la IA",
                [
                    "Privacidad",
                    "Calidad de resultados",
                    "Pérdida de control o confianza",
                    "Disponibilidad presupuestaria",
                    "Otro"
                ],
                key=f"riesgos_{idx}"
            )

        comentario = st.text_input(
            "Comentario adicional",
            key=f"com_{idx}"
        )

        st.session_state.actividades[idx] = {
            "Nombre": nombre,
            "Área": area,
            "Actividad general": actividad_general,
            "Actividad específica": actividad_especifica,
            "Repetitividad": repetitividad,
            "Tiempo": tiempo,
            "Beneficio IA": beneficio_ia,
            "Uso IA": uso_ia,
            "IA(s)": nombre_ia,
            "Plazo": plazo,
            "Riesgos": "; ".join(riesgos),
            "Comentario": comentario,
            "Fecha": datetime.now().isoformat()
        }


# =====================================
# AÑADIR ACTIVIDAD (TAMBIÉN AL FINAL)
# =====================================
st.divider()

st.button("➕ Añadir otra actividad (al final)", on_click=añadir_actividad)

# =====================================
# GUARDAR RESPUESTAS
# =====================================

st.divider()

if st.button("✅ Enviar respuestas"):

    if not st.session_state.actividades:
        st.warning("Debes añadir al menos una actividad.")
    else:
        df_nuevo = pd.DataFrame(st.session_state.actividades)

        try:
            df_existente = pd.read_csv(ARCHIVO_CSV)
            df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
        except FileNotFoundError:
            df_final = df_nuevo

        df_final.to_csv(ARCHIVO_CSV, index=False)

        st.success("¡Respuestas guardadas correctamente! Muchas gracias.")
        st.session_state.actividades = []
