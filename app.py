import streamlit as st
import time
from utils import obtener_preguntas
import streamlit.components.v1 as components


st.set_page_config(page_title="People Also Ask... More", page_icon=":eyes:")


# Agregar una imagen antes del título
st.image('https://i.imgur.com/ycoUH4F.png', use_container_width=True)
st.caption(f"[Creado por Damián Taubaso](https://www.linkedin.com/in/dtaubaso/)")
# Configurar la interfaz de usuario de Streamlit
st.title("Google's People Also Ask... More")



with st.expander('About this app'):
    st.write("""This app allows you to get many more results than the default four in Google's "People Also Ask" section. 

By clicking on each question, you can uncover more related questions. 

You can select your keyword, country, language, and the number of clicks the browser will perform.
""")

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
st.session_state.keyword = st.sidebar.text_input("Your keyword", st.session_state.keyword)
st.session_state.pais = st.sidebar.text_input("Country (two letters ISO format)", st.session_state.pais)
st.session_state.idioma = st.sidebar.text_input("Language (two letters ISO format)", st.session_state.idioma)
cantidad_clicks = st.sidebar.number_input("Clicks", min_value=1, max_value=20, value=2)

# Botones de búsqueda y reset
buscar, reset = st.sidebar.columns([1, 1])

if buscar.button("Search"):
    # Verifica si los campos no están vacíos
    if st.session_state.keyword and st.session_state.pais and st.session_state.idioma:
        # Llamar a la función de búsqueda con los parámetros dados
        with st.spinner('Processing...'):
            st.session_state.resultados = obtener_preguntas(st.session_state.keyword, st.session_state.pais, st.session_state.idioma, cantidad_clicks)
        st.session_state.search_performed = True
    else:
        # Mostrar mensaje de error si faltan campos requeridos
        st.error("Please fill out all the fields.")

if reset.button("Reset"):
    reset_fields()  # Llamar a la función para restablecer los campos y recargar la aplicación

# Mostrar los resultados si existen
if st.session_state.resultados:
    st.write("Results:")
    for i, resultado in enumerate(st.session_state.resultados):
        st.write(f"{i+1} - {resultado}")

    # Crear el contenido para el archivo de texto
    resultados_texto = "\n".join([res for res in st.session_state.resultados])
    
    kw_name = st.session_state.keyword.replace(" ", "_")
    # Botón para descargar el archivo de texto
    st.download_button(
        label="Download results as a text file.",
        data=resultados_texto,
        file_name= f'results_{kw_name}_{int(time.time())}.txt',  # Usar el timestamp Unix en el nombre del archivo
        mime='text/plain'
    )
elif st.session_state.search_performed:
    st.error("No results found")
