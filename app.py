import streamlit as st
import time
from utils import obtener_preguntas

st.title("Búsqueda de Resultados")
# Campos de entrada para los parámetros
keyword = st.text_input("Palabra clave (Keyword)")
pais = st.text_input("País")
idioma = st.text_input("Idioma")
cantidad_clicks = st.number_input("Cantidad de clicks", min_value=1, max_value=20, value=5)

# Inicializar st.session_state para los resultados si no existen
if 'resultados' not in st.session_state:
    st.session_state.resultados = None

# Botón para ejecutar la búsqueda
if st.button("Buscar"):
    if keyword and pais and idioma:
         # Limpiar resultados previos
        st.session_state.resultados = None
        with st.spinner('Procesando...'):
        # Llamar a la función de búsqueda con los parámetros dados
            st.session_state.resultados = obtener_preguntas(keyword, pais, idioma, cantidad_clicks)
    else:
        st.error("Por favor, complete todos los campos.")
if st.session_state.resultados is not None:
    # Mostrar los resultados
    st.write("Resultados:")
    for i, resultado in enumerate(st.session_state.resultados):
        st.write(f"{i+1} - {resultado}")
    resultados_texto = "\n".join([res for res in st.session_state.resultados])
    kw_name = keyword.replace(" ", "_")
    st.download_button(
            label="Descargar resultados como archivo de texto",
            data=resultados_texto,
            file_name=f'resultados_{kw_name}_{int(time.time())}.txt',
            mime='text/plain'
            )
