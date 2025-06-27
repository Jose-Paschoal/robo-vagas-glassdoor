# 🤖 Robô Scraper de Vagas de Dados – Glassdoor

Este projeto é um robô de scraping construído em Python com Selenium para **extrair vagas da área de dados** (como Analista de Dados, Cientista de Dados, BI, etc.) diretamente do site [Glassdoor](https://www.glassdoor.com/).

O objetivo é **automatizar a coleta de informações** relevantes sobre as vagas e disponibilizar esses dados para análise de mercado, como:

- **Título da vaga**
- **Nome da empresa**
- **Localidade**
- **Modalidade de trabalho** (remoto, híbrido, presencial)
- **Salário (quando disponível)**
- **Requisitos técnicos e comportamentais**
- **Tamanho da empresa** (futuramente)

---

## 📦 Tecnologias utilizadas

- Python 3.10+
- Selenium 4+
- Google Chrome
- ChromeDriver

---

## 📁 Organização do projeto

```bash
robo_vagas/
├── robo.py                # Script principal de automação
├── requirements.txt       # Bibliotecas necessárias
├── README.md              # Este arquivo
└── venv/                  # Ambiente virtual (não subir no GitHub)


⚙️ Requisitos para rodar
Ter o Google Chrome instalado

Baixar o ChromeDriver compatível com sua versão do Chrome

Python instalado (recomenda-se 3.10 ou superior)

(Opcional) Criar um ambiente virtual

🚀 Como executar
Clone este repositório:

bash
Copiar
Editar
git clone https://github.com/seu-usuario/robo_vagas.git
cd robo_vagas
(Opcional) Crie e ative um ambiente virtual:

bash
Copiar
Editar
python -m venv venv
venv\Scripts\activate  # Windows
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Verifique o caminho do chromedriver.exe dentro do robo.py

Execute o script:

bash
Copiar
Editar
python robo.py
🧪 O que o robô faz
Acessa o Glassdoor e realiza a busca por vagas na área de dados

Coleta os dados principais da vaga

Exibe no terminal informações como:

Título da vaga

Empresa

Local

Salário

(Futuramente) Irá salvar os dados em CSV para análise posterior

🛠️ Melhorias previstas
 Paginação automática

 Extração de descrição da vaga (para análise de requisitos técnicos)

 Classificação de modalidade de trabalho (remoto/presencial/híbrido)

 Classificação do tamanho da empresa

 Salvamento automático em .csv ou .xlsx

 Dashboard de visualização com Plotly/Streamlit/Power BI

📄 Licença
Este projeto é livre para fins de estudo, aprendizado e portfólio pessoal.
Caso deseje utilizar comercialmente ou em projetos maiores, entre em contato.