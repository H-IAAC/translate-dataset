import os

from google.cloud import translate_v2 as translate


def traduzir_texto(texto, idioma_destino, caminho_chave_api):
    """
    Realiza a tradução do texto para o idioma de destino utilizando a API do Google Translate.

    Args:
        texto (str): O texto a ser traduzido.
        idioma_destino (str): O idioma de destino para a tradução.
        caminho_chave_api (str):
            O caminho do arquivo JSON contendo a chave de API do Google Translate.

    Returns:
        str: O texto traduzido.

    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = caminho_chave_api
    client = translate.Client()
    traducao = client.translate(texto, target_language=idioma_destino)
    return traducao["translatedText"]
