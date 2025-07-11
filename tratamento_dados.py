# %%

# pós raspagem de dados - vamos começar enxergar

import pandas as pd
import numpy as np
import unicodedata

import json

import re

df = pd.read_csv('../ROBO_VAGAS/vagas_glassdoor.csv')

print(f'O dataset contém {df.shape[1]} colunas e {df.shape[0]} linhas')
df.head()

# %%

df.isna().sum()

# %%

df.describe()

# %%

## tratamentos dos dados

df.dtypes

# %%

df.columns

# %%

## tratar coluna 'titulo'

def tratar_titulo(titulo):
    if pd.isna(titulo):
        return{
            'titulo_tratado': None,
            'nivel': None,
        }
    
    # normalizando o titulo - retirando caracteres especiais - deixando minusculo

    titulo_limpo = unicodedata.normalize('NFKD', titulo).encode('ascii', 'ignore').decode('utf-8').lower()

    # checando se há nivel de senioridade nos títulos das vagas

    if 'estagio' in titulo_limpo:
        nivel = 'estagio'
    elif 'junior' in titulo_limpo or 'jr' in titulo_limpo:
        nivel = 'junior'
    elif 'pleno' in titulo_limpo or 'pl' in titulo_limpo:
        nivel = 'pleno'
    elif 'senior' in titulo_limpo or 'sr' in titulo_limpo:
        nivel = 'senior'
    elif 'especialista' in titulo_limpo:
        nivel = 'especialista'
    elif 'coordenador' in titulo_limpo or 'lead' in titulo_limpo:
        nivel = 'coordenador'
    elif 'gerente' in titulo_limpo:
        nivel = 'gerente'
    else:
        nivel = 'não informado'

    return {
        'titulo_tratado': titulo_limpo,
        'nivel': nivel
    }

# %%

## aplicando o tratamento

tratados = df['titulo'].apply(tratar_titulo).apply(pd.Series)

df = pd.concat([df, tratados], axis=1)

df.head()

# %%

df['local'].value_counts()

# %%

# tratamento da coluna 'local' - vamos checar casos de remoto, estado

with open('cidades.json', encoding='utf-8') as f:
    dados_estados = json.load(f)

cidade_para_estado = {}

for estado in dados_estados['estados']:
    sigla = estado['sigla']
    for cidade in estado['cidades']:
        cidade_para_estado[cidade.strip()] = sigla

# %%

# funcao

def tratar_local(local):
    if pd.isna(local):
        return{
            'cidade': None,
            'estado': None,
            'remoto': 0
        }

    # vagas remotas

    if any(palavra in local for palavra in ['remoto', 'home office', 'trabalho remoto']):
        return{
            'cidade': None,
            'estado': None,
            'remoto': 1
        }
    
    # checando se já possuimos estado junto ao nome de municipio

    partes = [p.strip() for p in local.split(',')]

    if len(partes) == 2:
        cidade = partes[0]
        estado = partes[1]

    else:
        cidade = partes[0]
        estado = cidade_para_estado.get(cidade, None)

    return {
        'cidade': cidade,
        'estado': estado,
        'remoto': 0
    }

# %%

# aplicando a funcao

tratados_local = df['local'].apply(tratar_local).apply(pd.Series)

# %%

df = pd.concat([df, tratados_local], axis=1)

df

# %%

df.isna().sum()

# %%

df['estado'].value_counts()

# %%

# mapeamento para correcao dos estados

mapeamento_estado_para_sigla = {
    "Acre": "AC",
    "Alagoas": "AL",
    "Amapá": "AP",
    "Amazonas": "AM",
    "Bahia": "BA",
    "Ceará": "CE",
    "Distrito Federal": "DF",
    "Espírito Santo": "ES",
    "Goiás": "GO",
    "Maranhão": "MA",
    "Mato Grosso": "MT",
    "Mato Grosso do Sul": "MS",
    "Minas Gerais": "MG",
    "Pará": "PA",
    "Paraíba": "PB",
    "Paraná": "PR",
    "Pernambuco": "PE",
    "Piauí": "PI",
    "Rio de Janeiro": "RJ",
    "Rio Grande do Norte": "RN",
    "Rio Grande do Sul": "RS",
    "Rondônia": "RO",
    "Roraima": "RR",
    "Santa Catarina": "SC",
    "São Paulo": "SP",
    "Sergipe": "SE",
    "Tocantins": "TO",
    # corrigindo variações
    "Parana": "PR",
    "Sao Paulo": "SP"
}

df['estado'] = df['estado'].replace(mapeamento_estado_para_sigla)

df.head()

# %%

df['estado'].value_counts()

# %%

df['remoto'].value_counts()

# %%

df['nivel'].value_counts()

# %%

# criando funcoes para mexer com a coluna de dias que a vaga foi publicada e criando uma coluna de faixas de dias

def converter_dias(valor):
    if pd.isna(valor):
        return None
    valor =  valor.lower().strip()

    if 'mais de' in valor:
        return 31
    
    elif 'h' in valor:
        return 1
    
    elif 'dia' in valor:
        try:
            return int(valor.split()[0])
        except:
            return None
        
    else:
        return None
    
# funcao para faixas

def criar_faixas(dias):
    if pd.isna(dias):
        return 'Desconhecido'
    elif dias <= 5:
        return '1 a 5 dias'
    elif dias <= 15:
        return '6 a 15 dias'
    elif dias <= 30:
        return '16 a 30 dias'
    else:
        return 'mais de 30 dias'
    
# %%

# aplicando as funcoes

df['dias_publicado'] = df['publicado_ha'].apply(converter_dias)
df['faixa_dias'] = df['dias_publicado'].apply(criar_faixas)

df.head()

# %%

# tentar enxergar alguns dados via crosstab

pd.crosstab(df['remoto'], df['faixa_dias'])

# %%  

# inserindo regioes

regioes = {
    'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Sul': ['PR', 'RS', 'SC']
}

def mapear_regiao(estado):
    if pd.isna(estado):
        return 'Desconhecido'
    estado = estado.upper()
    for regiao, estados in regioes.items():
        if estado in estados:
            return regiao
    return 'Outro'

df['regiao'] = df['estado'].apply(mapear_regiao)

df

# %%

pd.crosstab(df['regiao'], df['faixa_dias'])

# %%

pd.crosstab(df['remoto'], df['regiao'])

# %%

df[df['regiao']=='Desconhecido']['cidade'].value_counts()

# %%

pd.crosstab(df['remoto'], df['salario'])

# %%

df['salario'].value_counts()

# bagunca nos dados de faixas salariais

# %%

# a ideia agora é ajustar as faixas para algo mais fácil de ser lido

def extair_valor(salario):
    if 'não informado' in salario.lower():
        return np.nan
    
    # removendo textos e caracteres

    numeros = re.findall(r"R\$ (\d+\.?\d*) mil", salario)
    numeros_float = [float(n.replace('.', '').replace(',', '.')) for n in numeros]

    if len(numeros_float) == 1:
        return numeros_float[0] * 1000
    elif len (numeros_float) == 2:
        return (numeros_float[0] + numeros_float[1]) / 2 * 1000
    else:
        return np.nan
    
# %%

df['salario_valor'] = df['salario'].apply(extair_valor)

df

# %%

# faixas salariais

def classificar_faixas(salario):
    if pd.isna(salario):
        return 'Não informado'
    elif salario <= 5000:
        return '1k a 5k'
    elif salario <= 10000:
        return '5k a 10k'
    elif salario <=15000:
        return '10k a 15k'
    else:
        return 'Acima de 15k'
    
df['faixa_salarial'] = df['salario_valor'].apply(classificar_faixas)

df.head()

# %%

pd.crosstab(df['remoto'], df['faixa_salarial'])

# %%

pd.crosstab(df['regiao'], df['faixa_salarial'])

# %%

pd.crosstab(df['regiao'], df['nivel'])

# %%

pd.crosstab(df['nivel'], df['faixa_salarial'])

# %%

df.describe(include='all')

# %%

## salvando os dados

df.to_csv("vagas_glassdoor_tratado.csv", index=False, encoding='utf-8-sig')
