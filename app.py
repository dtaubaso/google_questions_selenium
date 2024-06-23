import streamlit as st
import time
from utils import obtener_preguntas

st.set_page_config(page_title="Google Questions", page_icon=":question:")

# Configurar la interfaz de usuario de Streamlit
st.title("Búsqueda de Resultados")

with st.expander('About this app'):
  st.write('This app shows the various ways on how you can layout your Streamlit app.')

st.sidebar.header('Input')
# Campos de entrada para los parámetros
keyword = st.sidebar.text_input("Palabra clave (Keyword)")
pais = st.sidebar.text_input("País")
idioma = st.sidebar.text_input("Idioma")
cantidad_clicks = st.sidebar.number_input("Cantidad de clicks", min_value=1, max_value=20, value=5)

if st.sidebar.button("Buscar"):
        # Verifica si los campos no están vacíos
        if keyword and pais and idioma:
            # Llamar a la función de búsqueda con los parámetros dados
            with st.spinner('Realizando búsqueda...'):
                resultados = obtener_preguntas(keyword, pais, idioma, cantidad_clicks)
            
            if resultados:
            # Mostrar los resultados
                st.write("Resultados:")
                for i, resultado in enumerate(resultados):
                    st.write(f"{i+1} - {resultado}")

                # Crear el contenido para el archivo de texto
                resultados_texto = "\n".join([res for res in resultados])
                    
                kw_name = keyword.replace(" ", "_")
                # Botón para descargar el archivo de texto
                st.download_button(
                        label="Descargar resultados como archivo de texto",
                        data=resultados_texto,
                        file_name= f'resultados_{kw_name}_{int(time.time())}.txt',  # Usar el timestamp Unix en el nombre del archivo
                        mime='text/plain'
                    )
            else:
                st.error("No se encontraron resultados")
        else:
            # Mostrar mensaje de error si faltan campos requeridos
            st.error("Por favor, complete todos los campos.")

