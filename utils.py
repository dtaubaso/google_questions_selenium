import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import urllib, time, logging

logging.basicConfig(level=logging.INFO)




def get_driver():
    # Instanciar el servicio de Selenium para Firefox
    service = Service()  # Si tienes un geckodriver específico, puedes indicar su ruta aquí

    # Configurar opciones para Firefox
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Ejecutar en modo headless
    options.add_argument("--disable-gpu")  # Deshabilitar GPU (opcional en Firefox)
    options.add_argument("--no-sandbox")  # Evita problemas en contenedores
    options.set_preference("dom.webdriver.enabled", False)  # Evitar detección de Selenium
    options.set_preference("useAutomationExtension", False)  # Similar a Chrome's disable-blink-features
    options.set_preference("javascript.enabled", True)  # Asegura que JavaScript esté habilitado (habilitado por defecto)

    # Retornar el controlador de Firefox
    return webdriver.Firefox(service=service, options=options)

def obtener_preguntas(kw, pais, lang, clicks):
  # url de google para generar una query
  base_url = "https://www.google.com/search?q="
  # codifico la kw como html
  query = urllib.parse.quote(kw)
  # genero la url
  url = f"{base_url}{query}&hl={lang}&gl={pais}"
  
  driver = get_driver()
  # "with" me va a cerrar el driver una vez que finalizó
  with driver:
    # voy a la url
    driver.get(url)
    time.sleep(1)
    logging.info(driver.page_source)
    # si no encuentra preguntas, detiene el proceso
    if len(driver.find_elements(By.XPATH, "//div[@jsname='pcRaIe']"))==0:
      return None
    # de lo contrario, hace click en los distintos elementos
    progress_bar = st.progress(0)
    for i in (range(clicks)):
      elemento_pregunta = driver.find_elements(By.XPATH, "//div[@jsname='pcRaIe']")
      elemento_pregunta[i].click()
      time.sleep(0.5)
      progress_bar.progress((i + 1) / clicks)
    # ahora busco los elementos con el texto
    preguntas = driver.find_elements(By.CLASS_NAME,"CSkcDe")
    texto_preguntas = []
    # itero por cada elemento y extraigo el texto
    for pregunta in preguntas:
      texto_preguntas.append(pregunta.text)
  return texto_preguntas
