import os
from bs4 import BeautifulSoup
import pandas as pd


# Caminho para a pasta com os arquivos HTML
pasta = "relatorios"
dados = []

# Para cada arquivo HTML na pasta
for nome_arquivo in os.listdir(pasta):
    if nome_arquivo.endswith(".html"):
        caminho = os.path.join(pasta, nome_arquivo)
        with open(caminho, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

            def extrair(texto):
                tag = soup.find('font', string=lambda x: x and texto in x)
                if tag:
                    td = tag.find_parent('td')
                    seguinte = td.find_next_sibling('td')
                    if seguinte:
                        valor = seguinte.get_text(strip=True).replace('\xa0', '')
                        return valor
                return ''

            numero = extrair('Nº do Processo:')
            marca = extrair('Marca:')
            situacao = extrair('Situação:')
            apresentacao = extrair('Apresentação:')
            natureza = extrair('Natureza:')
            apostila = extrair('Apostila')

            dados.append({
                'Nº do Processo': numero,
                'Marca': marca,
                'Situação': situacao,
                'Apresentação': apresentacao,
                'Natureza': natureza,
                'Apostila': apostila
            })

# Cria DataFrame
df = pd.DataFrame(dados)

# Salva em CSV
df.to_csv('relatorio_processo.csv', index=False, encoding='utf-8-sig')
print("✅ Arquivo 'relatorio_processo.csv' criado com sucesso.")
