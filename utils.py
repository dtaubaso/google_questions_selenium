import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By
import urllib, time


# instanciar el servicio de selenium
service = Service()
options = webdriver.ChromeOptions()
# agrego las opciones para que funcione en colab
options.add_argument("--headless")
options.add_argument("--disable-gpu")


def get_driver():
        return webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        )

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