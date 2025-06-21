import pandas as pd

# Carrega o arquivo original e remove colunas duplicadas
df_original = pd.read_csv('RESUMO de marcas coletivas-mt.csv', encoding='utf-8')

# Remove colunas duplicadas (mantém a primeira ocorrência de 'NO_PROCESS')
df_original = df_original.loc[:, ~df_original.columns.duplicated()]

# Carrega o arquivo extraído
df_extraido = pd.read_csv('relatorio_processo.csv', encoding='utf-8-sig')

# Normaliza colunas: remove espaços e garante que são strings com zeros à esquerda se necessário
def normaliza_processo(valor):
    try:
        return str(valor).strip().replace('\xa0', '').zfill(9)
    except:
        return ''

df_original['NO_PROCESS'] = df_original['NO_PROCESS'].apply(normaliza_processo)
df_extraido['Nº do Processo'] = df_extraido['Nº do Processo'].apply(normaliza_processo)

# Compara
processos_originais = set(df_original['NO_PROCESS'])
processos_extraidos = set(df_extraido['Nº do Processo'])

faltando = processos_originais - processos_extraidos

# Gera CSV dos faltantes
df_faltando = df_original[df_original['NO_PROCESS'].isin(faltando)]
df_faltando.to_csv('processos_faltando.csv', index=False, encoding='utf-8-sig')

# Mensagem final
print(f"⚠️ Foram encontrados {len(faltando)} processo(s) faltando.")
print("Arquivo 'processos_faltando.csv' criado com sucesso.")
