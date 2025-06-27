
# %%

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

caminho_driver = r"C:\Users\pasch\Desktop\chromedriver\chromedriver.exe"


# Configura o serviço do Chrome
servico = Service(caminho_driver)
driver = webdriver.Chrome(service=servico)

# Abre o link
url = "https://www.glassdoor.com.br/Vaga/brasil-analista-de-dados-vagas-SRCH_IL.0,6_IN36_KO7,24.htm"
driver.get(url)


wait = WebDriverWait(driver, 15)
# Espera os elementos com data-test='job-title' estarem presentes
titulos = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-test='job-title']")))

## enxergando os resultados encontrados

for titulo in titulos:
    print(titulo.text)


driver.quit()  # Fecha o navegador

