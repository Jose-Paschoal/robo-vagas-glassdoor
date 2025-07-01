
# %%

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException

import pandas as pd
import unicodedata

import time

# Caminho do driver
caminho_driver = r"C:\Users\pasch\Desktop\chromedriver\chromedriver.exe"

# Termos de busca
termos_busca = [
    "analista de dados", "data analyst", "cientista de dados", "data scientist",
    "engenheiro de dados", "data engineer", "analista de BI", "BI Analyst",
    "data architect", "arquiteto de dados", "data steward",
    "analytics engineer", "machine learning engineer", "engenheiro de machine learning",
    "especialista em dados", "analista de dados sênior", "product data analyst"
]

def gerar_url_glassdoor(termo_original):
    termo_normalizado = unicodedata.normalize('NFKD', termo_original).encode('ascii', 'ignore').decode('utf-8')
    termo_formatado = termo_normalizado.replace(' ', '-')
    return f"https://www.glassdoor.com.br/Vaga/brasil-{termo_formatado}-vagas-SRCH_IL.0,6_IN36_KO7,{7+len(termo_formatado)}.htm"

# Lista final
todas_vagas = []

for termo in termos_busca:
    print(f"\n🔍 Buscando por: {termo}\n")

    # Configura o Chrome
    servico = Service(caminho_driver)
    driver = webdriver.Chrome(service=servico)
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    # Acessa a URL
    url = gerar_url_glassdoor(termo)
    driver.get(url)

    # Clica em "Ver mais vagas"
    cliques = 0
    max_cliques = 25

    while cliques < max_cliques:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            botao = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='load-more']")))
            botao.click()
            cliques += 1
            print(f"Clique {cliques} no botão 'Ver mais vagas'")
            time.sleep(5)
        except (NoSuchElementException, ElementClickInterceptedException, TimeoutException):
            print("Botão 'Ver mais vagas' não encontrado ou limite de cliques atingido.")
            break

    # Coleta os elementos
    titulos = driver.find_elements(By.CSS_SELECTOR, "a[data-test='job-title']")
    empresas = driver.find_elements(By.CSS_SELECTOR, "span.EmployerProfile_compactEmployerName__9MGcV")
    locais = driver.find_elements(By.CSS_SELECTOR, "div[data-test='emp-location']")
    salarios = driver.find_elements(By.CSS_SELECTOR, "div[data-test='detailSalary']")
    publicacoes = driver.find_elements(By.CSS_SELECTOR, "div[data-test='job-age']")

    print(f"→ Títulos encontrados: {len(titulos)}")
    print(f"→ Empresas encontradas: {len(empresas)}")
    print(f"→ Locais encontrados: {len(locais)}")
    print(f"→ Publicações: {len(publicacoes)}")
    print(f"→ Salários: {len(salarios)}")

    # Constrói as vagas
    num_vagas = min(len(titulos), len(empresas), len(locais), len(publicacoes))
    for i in range(num_vagas):
        vaga = {
            'busca': termo,
            'titulo': titulos[i].text,
            'empresa': empresas[i].text,
            'local': locais[i].text,
            'publicado_ha': publicacoes[i].text,
            'salario': salarios[i].text if i < len(salarios) else 'Não informado'
        }
        todas_vagas.append(vaga)

    driver.quit()

# Salva no CSV
df = pd.DataFrame(todas_vagas)
print("\n✅ Coleta finalizada")
print(f"Total de vagas coletadas: {len(df)}")
df.to_csv("vagas_glassdoor.csv", index=False, encoding='utf-8-sig')


