import streamlit as st
import time
from utils import obtener_preguntas

# Configurar la interfaz de usuario de Streamlit
st.title("Búsqueda de Resultados")

# Campos de entrada para los parámetros
keyword = st.text_input("Palabra clave (Keyword)")
pais = st.selectbox("País", ["Argentina", "España", "México", "Estados Unidos", "Otro"])
idioma = st.selectbox("Idioma", ["Español", "Inglés", "Otro"])
cantidad_clicks = st.number_input("Cantidad de clicks", min_value=1, max_value=100, value=10)

# Botón de reset para limpiar resultados y reiniciar campos de búsqueda
if st.button("Reset"):
    keyword = ""
    pais = ""
    idioma = ""
    cantidad_clicks = 10
    st.session_state.resultados = None

# Inicializar st.session_state para los resultados si no existen
if 'resultados' not in st.session_state:
    st.session_state.resultados = None

# Botón para ejecutar la búsqueda
if st.button("Buscar"):
    if keyword and pais and idioma:
        # Limpiar resultados previos usando el contenedor
        st.session_state.resultados = None

        # Llamar a la función de búsqueda con los parámetros dados
        with st.spinner('Realizando búsqueda...'):
            st.session_state.resultados = obtener_preguntas(keyword, pais, idioma, cantidad_clicks)
    else:
        st.error("Por favor, complete todos los campos.")

# Mostrar los resultados si existen en st.session_state
if st.session_state.resultados is not None:
    if st.session_state.resultados:  # Verificar si la lista no está vacía
        st.write("Resultados:")
        for i, resultado in enumerate(st.session_state.resultados):
            st.write(f"{i+1} - {resultado}")

        # Crear el contenido para el archivo de texto
        resultados_texto = "\n".join([res for res in st.session_state.resultados])
        
        kw_name = keyword.replace(" ", "_")
        # Botón para descargar el archivo de texto
        st.download_button(
            label="Descargar resultados como archivo de texto",
            data=resultados_texto,
            file_name= f'resultados_{kw_name}_{int(time.time())}.txt',  # Usar el timestamp Unix en el nombre del archivo
            mime='text/plain'
        )
    else:
        st.warning("No hubo resultados para los parámetros de búsqueda ingresados.")
else:
    st.info("Ingrese los parámetros de búsqueda y presione 'Buscar'.")