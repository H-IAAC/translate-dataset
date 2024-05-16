"""
Este módulo contém funções para traduzir arquivos CSV presentes em uma pasta
para o idioma de destino utilizando a API do Google Translate.
Os arquivos traduzidos são salvos em uma pasta de saída.

Funções:
- traduzir_csv: Traduz os arquivos CSV presentes na pasta de entrada.
- obter_arquivos_csv: Obtém a lista de arquivos CSV presentes em uma pasta.
- traduzir_arquivo_csv: Traduz um arquivo CSV para o idioma de destino.
- traduzir_texto:
    Realiza a tradução de um texto para o idioma de destino utilizando a
    API do Google Translate.

Exemplo de uso:
    O módulo pode ser executado como um script, solicitando ao usuário os
    parâmetros necessários:

    $ python nome_do_modulo.py

    Em seguida, o usuário será solicitado a fornecer o caminho da pasta de
    entrada, o caminho da pasta de saída, o idioma de destino e o caminho
    do arquivo JSON contendo a chave de API do Google Translate.
"""

import csv
import logging
import os

from google.cloud import translate_v2 as translate

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def traduzir_csv(
    caminho_pasta_entrada,
    caminho_pasta_saida=None,
    idioma_destino="pt",
    caminho_chave_api=None,
):
    """
    Traduz os arquivos CSV presentes na pasta de entrada para o idioma de
    destino e salva os arquivos traduzidos na pasta de saída.

    Args:
        caminho_pasta_entrada (str):
            O caminho da pasta de entrada contendo os arquivos CSV a serem
            traduzidos.
        caminho_pasta_saida (str, optional):
            O caminho da pasta de saída onde os arquivos traduzidos serão
            salvos.

            Se não for fornecido, será criada uma pasta "traducao" dentro
            da pasta de entrada.
        idioma_destino (str, optional):
            O idioma de destino para a tradução. Default é "pt" (português).
        caminho_chave_api (str, optional):
            O caminho do arquivo JSON contendo a chave de API do Google
            Translate.

    """
    if not os.path.exists(caminho_pasta_entrada):
        logging.error("A pasta de entrada '%s' não existe.", caminho_pasta_entrada)
        return

    if caminho_pasta_saida is None:
        caminho_pasta_saida = os.path.join(caminho_pasta_entrada, "traducao")
    elif not os.path.exists(caminho_pasta_saida):
        os.makedirs(caminho_pasta_saida)

    arquivos_csv = obter_arquivos_csv(caminho_pasta_entrada)

    for arquivo_csv in arquivos_csv:
        caminho_arquivo_entrada = os.path.join(caminho_pasta_entrada, arquivo_csv)
        caminho_arquivo_saida = os.path.join(caminho_pasta_saida, arquivo_csv)

        traduzir_arquivo_csv(
            caminho_arquivo_entrada,
            caminho_arquivo_saida,
            idioma_destino,
            caminho_chave_api,
        )


def obter_arquivos_csv(caminho_pasta):
    """
    Obtém a lista de arquivos CSV presentes na pasta especificada.

    Args:
        caminho_pasta (str): O caminho da pasta.

    Returns:
        list: Lista de nomes dos arquivos CSV presentes na pasta.

    """
    return [
        arquivo for arquivo in os.listdir(caminho_pasta) if arquivo.endswith(".csv")
    ]


def traduzir_arquivo_csv(
    caminho_arquivo_entrada, caminho_arquivo_saida, idioma_destino, caminho_chave_api
):
    """
    Traduz o arquivo CSV de entrada para o idioma de destino e salva o arquivo
    traduzido.

    Args:
        caminho_arquivo_entrada (str): O caminho do arquivo CSV de entrada.
        caminho_arquivo_saida (str): O caminho do arquivo CSV de saída
                                     traduzido.
        idioma_destino (str): O idioma de destino para a tradução.
        caminho_chave_api (str):
            O caminho do arquivo JSON contendo a chave de API do Google
            Translate.

    """
    traducoes = []

    with open(caminho_arquivo_entrada, "r", encoding="utf-8") as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)

        for linha in leitor_csv:
            texto = linha[0]
            traducao = traduzir_texto(texto, idioma_destino, caminho_chave_api)
            traducoes.append([traducao])

    with open(caminho_arquivo_saida, "w", newline="", encoding="utf-8") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerows(traducoes)

    logging.info("Arquivo CSV traduzido gerado: %s", caminho_arquivo_saida)


def traduzir_texto(texto, idioma_destino, caminho_chave_api):
    """
    Realiza a tradução do texto para o idioma de destino utilizando a
    API do Google Translate.

    Args:
        texto (str): O texto a ser traduzido.
        idioma_destino (str): O idioma de destino para a tradução.
        caminho_chave_api (str):
            O caminho do arquivo JSON contendo a chave de API do
            Google Translate.

    Returns:
        str: O texto traduzido.

    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = caminho_chave_api
    client = translate.Client()
    traducao = client.translate(texto, target_language=idioma_destino)
    return traducao["translatedText"]


if __name__ == "__main__":
    # Configuração dos parâmetros de tradução
    caminho_pasta_entrada_original = input("Digite o caminho da pasta de arquivo CSV: ")
    caminho_pasta_saida_traduzida = input(
        "Digite o caminho do destino do arquivo CSV traduzido: "
    )
    idioma_traducao = input("Digite o idioma de tradução: ")
    caminho_chave_api_atual = input("Digite o caminho da chave API: ")

    # Execução da tradução
    traduzir_csv(
        caminho_pasta_entrada_original,
        caminho_pasta_saida_traduzida,
        idioma_traducao,
        caminho_chave_api_atual,
    )
