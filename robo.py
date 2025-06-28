
# %%

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

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
empresas = driver.find_elements(By.CSS_SELECTOR, "span.EmployerProfile_compactEmployerName__9MGcV")
locais = driver.find_elements(By.CSS_SELECTOR, "div[data-test='emp-location']")
salarios = driver.find_elements(By.CSS_SELECTOR, "div[data-test='detailSalary']")
publicacoes = driver.find_elements(By.CSS_SELECTOR, "div[data-test='job-age']")

## enxergando os resultados encontrados

## criar lista de vagas

vagas = []
num_vagas = min(len(titulos), len(empresas), len(locais), len(publicacoes))


for i in range(num_vagas):
    vaga = {
        'titulo': titulos[i].text,
        'empresa': empresas[i].text,
        'local': locais[i].text,
        'pubicado_ha': publicacoes[i].text,
        'salario': salarios[i].text if i < len(salarios) else 'Não informado'
    }
    vagas.append(vaga)


driver.quit()  # Fecha o navegador

## criar o dataframe

df = pd.DataFrame(vagas)
print(df.head())

