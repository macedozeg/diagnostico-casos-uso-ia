import streamlit as st

st.set_page_config(
    page_title="Diagnóstico de Casos de Uso de IA",
    layout="wide"
)

st.title("Diagnóstico operativo de Casos de Uso de IA")
st.write(
    "Este cuestionario sirve para identificar actividades que pueden beneficiarse del uso de IA."
)

st.header("Identificación del respondiente")

nombre = st.text_input("Nombre y apellidos *")
area = st.text_input("Área / Equipo")

if not nombre:
    st.warning("Por favor, indica tu nombre para continuar.")
    st.stop()

st.success("Identificación completada. Continúa con el cuestionario 👇")

st.divider()

st.write(
    "👉 En el siguiente paso añadiremos aquí el formulario completo de actividades."
)
