# %%

# pós raspagem de dados - vamos começar enxergar

import pandas as pd
import numpy as np
import unicodedata

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
