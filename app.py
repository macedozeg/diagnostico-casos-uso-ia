import streamlit as st
import pandas as pd
from datetime import datetime

# CONFIG
st.set_page_config(page_title="Diagnóstico IA", layout="wide")
ARCHIVO_CSV = "respuestas_diagnostico_ia.csv"

# ACTIVIDADES
ACTIVIDADES = {
    "Procesos administrativos internos": [
        "Gestión de correos electrónicos",
        "Transcripción y resumen de reuniones",
        "Bases de datos (Excel)",
        "Planificación interna",
        "Recordatorios",
        "Justificaciones de gastos",
        "Archivo documentación",
        "Informes de actividad"
    ],
    "Convocatorias": [
        "Revisión de bases",
        "Preparación propuestas",
        "Búsqueda de información",
        "Resolución de dudas"
    ],
    "Proyectos": [
        "Memoria técnico-económica",
        "Scouting resultados"
    ],
    "Legal": [
        "Revisión de contratos",
        "Comparación versiones",
        "Marco legislativo"
    ]
}

# TÍTULO
st.title("Diagnóstico de Casos de Uso de IA")
st.markdown("""
**Instrucciones:**

1) Este cuestionario permite identificar actividades susceptibles de mejora mediante tecnologías de automatización e inteligencia artificial.
2) Primero indícanos tus datos, luego añade todas las actividades que consideres susceptibles del uso de IA (has click en añadir actividad) .
3) Al añadir una actividad, primero selecciona la actividad general y según ello elige la actividad específica asociada. Completa la información solicitada.
4) Finalmente, luego de añadir todas las actividades que creas conveniente, haz click en Enviar respuestas.

📩 Dudas: macedoma@unican.es
""")
# IDENTIFICACIÓN
st.header("Identificación")

nombre = st.text_input("Nombre *")
area = st.text_input("Área")

if not nombre:
    st.warning("Introduce tu nombre para continuar")
    st.stop()

st.success("✅ Continúa con las actividades")
st.divider()

# ESTADO
if "actividades" not in st.session_state:
    st.session_state.actividades = []

def añadir():
    st.session_state.actividades.append({})

# BOTÓN INICIAL
if len(st.session_state.actividades) == 0:
    st.button("➕ Añadir actividad", on_click=añadir)

# FORMULARIO
for i in range(len(st.session_state.actividades)):

    with st.container(border=True):

        st.subheader(f"Actividad {i+1}")

        ag = st.selectbox("Actividad general", list(ACTIVIDADES.keys()), key=f"ag{i}")
        ae = st.selectbox("Actividad específica", ACTIVIDADES[ag], key=f"ae{i}")

        rep = st.selectbox("Repetitividad", ["Bajo", "Medio", "Alto"], key=f"rep{i}")
        tiempo = st.selectbox("Consumo de tiempo", ["Bajo", "Medio", "Alto"], key=f"time{i}")

        equipo = st.selectbox(
            "¿Participan varias personas del equipo?",
            ["No", "Sí"],
            key=f"equipo{i}"
        )

        beneficio = st.selectbox("¿Puede beneficiarse de IA?", ["No", "Sí"], key=f"bia{i}")

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

                herramienta = st.text_input(
                    "IA principal utilizada",
                    key=f"herr{i}"
                )

                licencia = st.selectbox(
                    "Licencia",
                    ["Gratis", "De Pago"],
                    key=f"lic{i}"
                )

                if licencia == "De Pago":
                    coste = st.number_input("Coste anual (€)", 0, key=f"cost{i}")

            mejoras = st.text_area("Mejoras que aportaría la IA", key=f"mej{i}")

            implantacion = st.selectbox(
                "Nivel de implantación",
                [
                    "Corto plazo: impacto inmediato",
                    "Medio plazo: requiere preparación",
                    "Largo plazo: transformación estructural"
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

# BOTÓN FINAL
if len(st.session_state.actividades) > 0:
    st.divider()
    st.button("➕ Añadir otra actividad", on_click=añadir)

# GUARDAR
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
