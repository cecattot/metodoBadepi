from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pandas as pd

# Carrega os dados do arquivo CSV
df = pd.read_csv("RESUMO de marcas coletivas-mt.csv", encoding='utf-8', sep=None, engine='python')
codigos = df["NO_PROCESS"].astype(str).tolist()
#codigos = ["905058631"]

# Garante que a pasta exista
os.makedirs("relatorios", exist_ok=True)

# Configurações do navegador
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # opcional: roda o navegador invisivelmente
driver = webdriver.Chrome(options=options)

try:
    # Etapa 1: Acessa a página de login
    driver.get("https://busca.inpi.gov.br/pePI/")

    # Espera os campos de login carregarem e insere os dados
    usuario = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="principal"]/form/table/tbody/tr[1]/td[2]/font/input'))
    )
    senha = driver.find_element(By.XPATH, '//*[@id="principal"]/form/table/tbody/tr[2]/td[2]/font/input')

    usuario.send_keys("")
    senha.send_keys("")

    # Submete o formulário de login
    senha.submit()

    driver.get("https://busca.inpi.gov.br/pePI/jsp/marcas/Pesquisa_num_processo.jsp")

    # Etapa 2: Processa cada código
    for codigo in codigos:
        try:
            # Espera o campo do formulário carregar e preenche
            campo_processo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="principal"]/table[2]/tbody/tr[4]/td[2]/font/input'))
            )
            campo_processo.clear()
            campo_processo.send_keys(codigo)
            campo_processo.submit()

            html = driver.find_element(By.XPATH, '//*[@id="principal"]').get_attribute('outerHTML')
            if 'AVISO' in html:
                print("aqui")
                html_content = driver.find_element(By.XPATH, '//*[@id="principal"]/table[4]/tbody').get_attribute(
                    'outerHTML')
                # Salva o conteúdo da página
                with open(f"relatorios/{codigo}.html", "w", encoding="utf-8") as f:
                    f.write(html_content)

                print(f"✅ Relatório salvo: relatorios/{codigo}.html")
            else:

                # Aguarda o link de detalhes do processo aparecer
                link_detalhes = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="principal"]/table[3]/tbody/tr[2]/td[2]/font/a'))
                )
                link_detalhes.click()
                # Aguarda o carregamento completo da nova página
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="principal"]'))
                )
                html_content = driver.find_element(By.XPATH, '//*[@id="principal"]').get_attribute('outerHTML')

                # Salva o conteúdo da página
                with open(f"relatorios/{codigo}.html", "w", encoding="utf-8") as f:
                    f.write(html_content)

                print(f"✅ Relatório salvo: relatorios/{codigo}.html")
            # Volta para a página de pesquisa para o próximo
            driver.get("https://busca.inpi.gov.br/pePI/jsp/marcas/Pesquisa_num_processo.jsp")

        except Exception as e:
            print(f"⚠️ Erro ao processar {codigo}: {e}")

finally:
    driver.quit()
