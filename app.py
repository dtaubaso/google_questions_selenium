import streamlit as st
import time
from utils import obtener_preguntas

st.set_page_config(page_title="Google Questions", page_icon=":question:")

# Configurar la interfaz de usuario de Streamlit
st.title("Búsqueda de Resultados")

with st.expander('About this app'):
    st.write('This app shows the various ways on how you can layout your Streamlit app.')

st.sidebar.header('Input')

# Inicializar los estados de los campos si no existen
if 'keyword' not in st.session_state:
    st.session_state.keyword = ''
if 'pais' not in st.session_state:
    st.session_state.pais = ''
if 'idioma' not in st.session_state:
    st.session_state.idioma = ''
if 'resultados' not in st.session_state:
    st.session_state.resultados = []
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False

# Función para restablecer los campos de entrada
def reset_fields():
    st.session_state.keyword = ''
    st.session_state.pais = ''
    st.session_state.idioma = ''
    st.session_state.resultados = []
    st.session_state.search_performed = False
    st.rerun()  # Recargar la aplicación para actualizar la UI

# Campos de entrada para los parámetros
st.session_state.keyword = st.sidebar.text_input("Palabra clave (Keyword)", st.session_state.keyword)
st.session_state.pais = st.sidebar.text_input("País", st.session_state.pais)
st.session_state.idioma = st.sidebar.text_input("Idioma", st.session_state.idioma)
cantidad_clicks = st.sidebar.number_input("Cantidad de clicks", min_value=1, max_value=20, value=5)

# Botones de búsqueda y reset
buscar, reset = st.sidebar.columns([1, 1])

if buscar.button("Buscar"):
    # Verifica si los campos no están vacíos
    if st.session_state.keyword and st.session_state.pais and st.session_state.idioma:
        # Llamar a la función de búsqueda con los parámetros dados
        with st.spinner('Realizando búsqueda...'):
            st.session_state.resultados = obtener_preguntas(st.session_state.keyword, st.session_state.pais, st.session_state.idioma, cantidad_clicks)
        st.session_state.search_performed = True
    else:
        # Mostrar mensaje de error si faltan campos requeridos
        st.error("Por favor, complete todos los campos.")

if reset.button("Reset"):
    reset_fields()  # Llamar a la función para restablecer los campos y recargar la aplicación

# Mostrar los resultados si existen
if st.session_state.resultados:
    st.write("Resultados:")
    for i, resultado in enumerate(st.session_state.resultados):
        st.write(f"{i+1} - {resultado}")

    # Crear el contenido para el archivo de texto
    resultados_texto = "\n".join([res for res in st.session_state.resultados])
    
    kw_name = st.session_state.keyword.replace(" ", "_")
    # Botón para descargar el archivo de texto
    st.download_button(
        label="Descargar resultados como archivo de texto",
        data=resultados_texto,
        file_name= f'resultados_{kw_name}_{int(time.time())}.txt',  # Usar el timestamp Unix en el nombre del archivo
        mime='text/plain'
    )
elif st.session_state.search_performed:
    st.error("No se encontraron resultados")
