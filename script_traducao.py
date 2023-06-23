import csv
import os
from google.cloud import translate_v2 as translate

def traduzir_csv(caminho_pasta_entrada, caminho_pasta_saida=None, idioma_destino='pt', caminho_chave_api=None):
    if not os.path.exists(caminho_pasta_entrada):
        print(f"A pasta de entrada '{caminho_pasta_entrada}' não existe.")
        return

    if caminho_pasta_saida is None:
        caminho_pasta_saida = os.path.join(caminho_pasta_entrada, "traducao")
    elif not os.path.exists(caminho_pasta_saida):
        os.makedirs(caminho_pasta_saida)

    arquivos_csv = obter_arquivos_csv(caminho_pasta_entrada)

    for arquivo_csv in arquivos_csv:
        caminho_arquivo_entrada = os.path.join(caminho_pasta_entrada, arquivo_csv)
        caminho_arquivo_saida = os.path.join(caminho_pasta_saida, arquivo_csv)

        traduzir_arquivo_csv(caminho_arquivo_entrada, caminho_arquivo_saida, idioma_destino, caminho_chave_api)

def obter_arquivos_csv(caminho_pasta):
    return [arquivo for arquivo in os.listdir(caminho_pasta) if arquivo.endswith('.csv')]

def traduzir_arquivo_csv(caminho_arquivo_entrada, caminho_arquivo_saida, idioma_destino, caminho_chave_api):
    traducoes = []

    with open(caminho_arquivo_entrada, 'r', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)

        for linha in leitor_csv:
            texto = linha[0]
            traducao = traduzir_texto(texto, idioma_destino, caminho_chave_api)
            traducoes.append([traducao])

    with open(caminho_arquivo_saida, 'w', newline='', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerows(traducoes)

    print(f"Arquivo CSV traduzido gerado: {caminho_arquivo_saida}")

def traduzir_texto(texto, idioma_destino, caminho_chave_api):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = caminho_chave_api
    client = translate.Client()
    traducao = client.translate(texto, target_language=idioma_destino)
    return traducao['translatedText']


# Exemplo de uso
caminho_pasta_entrada = 'train_saida'  # Substitua pelo caminho real da pasta de entrada
caminho_pasta_saida = 'traducao_final'  # Substitua pelo caminho real da pasta de saída (opcional)
idioma_destino = 'pt'  # Substitua pelo idioma de destino desejado (exemplo: 'pt' para português)
caminho_chave_api = 'skilful-answer-390621-00fe41eacd9e.json'  # Substitua pelo caminho real do arquivo JSON da chave de API

traduzir_csv(caminho_pasta_entrada, caminho_pasta_saida, idioma_destino, caminho_chave_api)