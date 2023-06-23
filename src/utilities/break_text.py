import pandas as pd
import csv
import logging
import os
import glob
from typing import List
from google.cloud import translate_v2 as translate


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def verificar_e_dividir_limite_caracteres_csv(
    caminho_arquivo: str,
    nome_coluna: str,
    tamanho_maximo: int,
    num_linhas: int,
    pasta_saida: str,
    nome_arquivo: str
) -> None:
    """
    Verifica o limite de caracteres por chamada em um arquivo CSV e o divide em partes menores, se necessário.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV.
        nome_coluna (str): O nome da coluna a ser verificada.
        tamanho_maximo (int): O tamanho máximo de caracteres por chamada.
        num_linhas (int): O número máximo de linhas a serem lidas.
        pasta_saida (str): O caminho para a pasta de saída dos arquivos gerados.
        nome_arquivo (str): O nome do arquivo base para gerar as subpastas.

    Raises:
        FileNotFoundError: Se o arquivo CSV não existe.
    """
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"O arquivo CSV '{caminho_arquivo}' não existe.")

    nome_arquivo_base = os.path.splitext(os.path.basename(caminho_arquivo))[0]

    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    pasta_arquivo = os.path.join(pasta_saida, nome_arquivo)
    if not os.path.exists(pasta_arquivo):
        os.makedirs(pasta_arquivo)
    else:
        # Remover os arquivos existentes na pasta de saída
        arquivos_existentes = glob.glob(os.path.join(pasta_arquivo, '*.csv'))
        for arquivo in arquivos_existentes:
            os.remove(arquivo)

    if contar_linhas_csv(caminho_arquivo) > 1000:
        dividir_texto_pandas(caminho_arquivo, nome_coluna, tamanho_maximo, num_linhas, pasta_arquivo, nome_arquivo_base)
    else:
        dividir_texto_csv(caminho_arquivo, nome_coluna, tamanho_maximo, num_linhas, pasta_arquivo, nome_arquivo_base)

def contar_linhas_csv(caminho_arquivo: str) -> int:
    """
    Conta o número de linhas em um arquivo CSV.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV.

    Returns:
        int: O número de linhas no arquivo CSV.
    """
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_csv:
        total_linhas = sum(1 for _ in arquivo_csv)
    return total_linhas

def dividir_texto_csv(
    caminho_arquivo: str,
    nome_coluna: str,
    tamanho_maximo: int,
    num_linhas: int,
    pasta_saida: str,
    nome_arquivo_base: str
) -> None:
    """
    Divide o texto em partes menores e gera arquivos CSV correspondentes.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV.
        nome_coluna (str): O nome da coluna a ser verificada.
        tamanho_maximo (int): O tamanho máximo de caracteres por chamada.
        num_linhas (int): O número máximo de linhas a serem lidas.
        pasta_saida (str): O caminho para a pasta de saída dos arquivos gerados.
        nome_arquivo_base (str): O nome do arquivo base para gerar as subpastas.
    """
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.DictReader(arquivo_csv)
        total_linhas = min(num_linhas, sum(1 for _ in leitor_csv))
        arquivo_csv.seek(0)
        next(leitor_csv)  # Ignorar o cabeçalho

        linha_atual = 1

        for linha in leitor_csv:
            if linha_atual > num_linhas:
                break

            texto = linha[nome_coluna]
            subdivisoes = dividir_texto_em_subtextos(texto, tamanho_maximo)

            for i, subtexto in enumerate(subdivisoes):
                nome_arquivo = f"{nome_arquivo_base}_linha{linha_atual}"

                if len(subdivisoes) > 1:
                    nome_arquivo += f"_parte{i+1}"

                nome_arquivo += ".csv"
                caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)

                with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv_saida:
                    escritor_csv = csv.writer(arquivo_csv_saida)
                    escritor_csv.writerow([nome_coluna])
                    escritor_csv.writerow([subtexto])

                logging.info(f"Arquivo CSV gerado: {caminho_arquivo}")

            linha_atual += 1
            monitorar_progresso(linha_atual, total_linhas)

def dividir_texto_pandas(
    caminho_arquivo: str,
    nome_coluna: str,
    tamanho_maximo: int,
    num_linhas: int,
    pasta_saida: str,
    nome_arquivo_base: str
) -> None:
    """
    Divide o texto em partes menores usando a biblioteca pandas e gera arquivos CSV correspondentes.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV.
        nome_coluna (str): O nome da coluna a ser verificada.
        tamanho_maximo (int): O tamanho máximo de caracteres por chamada.
        num_linhas (int): O número máximo de linhas a serem lidas.
        pasta_saida (str): O caminho para a pasta de saída dos arquivos gerados.
        nome_arquivo_base (str): O nome do arquivo base para gerar as subpastas.
    """
    df = pd.read_csv(caminho_arquivo, encoding='utf-8', nrows=num_linhas)
    total_linhas = min(num_linhas, len(df))
    linha_atual = 1

    for _, linha in df.iterrows():
        texto = linha[nome_coluna]
        subdivisoes = dividir_texto_em_subtextos(texto, tamanho_maximo)

        for i, subtexto in enumerate(subdivisoes):
            nome_arquivo = f"{nome_arquivo_base}_linha{linha_atual}"

            if len(subdivisoes) > 1:
                nome_arquivo += f"_parte{i+1}"

            nome_arquivo += ".csv"
            caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)

            with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv_saida:
                escritor_csv = csv.writer(arquivo_csv_saida)
                escritor_csv.writerow([nome_coluna])
                escritor_csv.writerow([subtexto])

            logging.info(f"Arquivo CSV gerado: {caminho_arquivo}")

        linha_atual += 1
        monitorar_progresso(linha_atual, total_linhas)

def dividir_texto_em_subtextos(texto: str, tamanho_maximo: int) -> List[str]:
    """
    Divide um texto em partes menores respeitando o tamanho máximo de caracteres por chamada.

    Args:
        texto (str): O texto a ser dividido.
        tamanho_maximo (int): O tamanho máximo de caracteres por chamada.

    Returns:
        List[str]: A lista de subtextos divididos.
    """
    subtextos = []
    palavras = texto.split()
    subtexto_atual = ""

    for palavra in palavras:
        if len(subtexto_atual) + len(palavra) + 1 <= tamanho_maximo:
            subtexto_atual += palavra + " "
        else:
            subtextos.append(subtexto_atual.strip())
            subtexto_atual = palavra + " "

    if subtexto_atual:
        subtextos.append(subtexto_atual.strip())

    return subtextos

def monitorar_progresso(linha_atual: int, total_linhas: int) -> None:
    """
    Monitora o progresso do processamento.

    Args:
        linha_atual (int): O número da linha atual.
        total_linhas (int): O número total de linhas.

    Returns:
        None
    """
    porcentagem_conclusao = (linha_atual / total_linhas) * 100
    logging.info(f"Progresso: {linha_atual}/{total_linhas} linhas processadas ({porcentagem_conclusao:.4f}%)")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    caminho_arquivo = input("Digite o caminho para o arquivo CSV: ")
    nome_coluna = input("Digite o nome da coluna a ser verificada: ")
    tamanho_maximo = int(input("Digite o tamanho máximo de caracteres por chamada: "))
    num_linhas = int(input("Digite o número máximo de linhas a serem lidas: "))
    nome_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))[0]

    pasta_saida = input("Digite o caminho para a pasta de saída dos arquivos gerados: ")

    verificar_e_dividir_limite_caracteres_csv(caminho_arquivo, nome_coluna, tamanho_maximo, num_linhas, pasta_saida, nome_arquivo)