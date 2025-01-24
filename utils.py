import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import urllib, time, logging

logging.basicConfig(level=logging.INFO)



def obtener_preguntas(kw, pais, lang, clicks):
  service = Service()  # Si tienes un geckodriver específico, puedes indicar su ruta aquí
    # Configurar opciones para Firefox
  options = webdriver.ChromeOptions()
  options.add_argument("--headless=new")
  options.add_argument("--disable-gpu")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-blink-features=AutomationControlled")
  options.add_argument("--enable-javascript")
  driver = webdriver.Chrome(service=service, options=options)

  # url de google para generar una query
  base_url = "https://www.google.com/search?q="
  # codifico la kw como html
  query = urllib.parse.quote(kw)
  # genero la url
  url = f"{base_url}{query}&hl={lang}&gl={pais}"
  
  # "with" me va a cerrar el driver una vez que finalizó
  with driver:
    # voy a la url
    driver.get(url)
    driver.implicitly_wait(3)
    time.sleep(0.5)
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
