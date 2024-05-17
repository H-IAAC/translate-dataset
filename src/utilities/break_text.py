"""Este módulo contém funções para verificar o limite de caracteres.

Ele também fornece funções de utilidade para contar o número de linhas em um
arquivo CSV, dividir um texto em subtextos com base em um limite de tamanho
e monitorar o progresso do processamento.

Funções:
- verificar_e_dividir_limite_caracteres_csv:
    Verifica o limite de caracteres em um arquivo CSV e divide o arquivo
    se necessário.

- contar_linhas_csv: Conta o número de linhas em um arquivo CSV.

- dividir_texto_csv:
    Divide o texto de um arquivo CSV em partes menores e gera arquivos
    CSV correspondentes.

- dividir_texto_pandas:
    Divide o texto de um arquivo CSV usando pandas e gera arquivos CSV
    correspondentes.

- dividir_texto_em_subtextos:
    Divide um texto em subtextos com base em um limite de tamanho.

- monitorar_progresso:
    Monitora o progresso do processamento e imprime a porcentagem de
    conclusão.

Exemplo de uso:
    Este módulo pode ser usado como um script para verificar e dividir
    um arquivo CSV a partir da linha de comando:

    $ python nome_do_modulo.py

    Em seguida, o usuário será solicitado a fornecer informações sobre
    o arquivo CSV e as configurações desejadas.
"""

import csv
import glob
import logging
import os
from typing import List

import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class CSVProcessor:
    """Classe para processar arquivos CSV."""

    def __init__(
        self,
        caminho_arquivo: str,
        nome_coluna: str,
        tamanho_maximo: int,
        num_linhas: int,
        pasta_saida: str,
        nome_arquivo: str,
    ):
        """
        Inicializa o processador CSV com os parâmetros fornecidos.

        Args:
            caminho_arquivo (str): O caminho do arquivo CSV.
            nome_coluna (str): O nome da coluna a ser processada.
            tamanho_maximo (int): O tamanho máximo para a divisão do texto.
            num_linhas (int): O número máximo de linhas a serem lidas no CSV.
            pasta_saida (str): O diretório onde o arquivo CSV processado será
                               armazenado.
            nome_arquivo (str): O nome do arquivo CSV processado.
        """
        self.caminho_arquivo = caminho_arquivo
        self.nome_coluna = nome_coluna
        self.tamanho_maximo = tamanho_maximo
        self.num_linhas = num_linhas
        self.pasta_saida = pasta_saida
        self.nome_arquivo = nome_arquivo

    def verificar_e_dividir_limite_caracteres_csv(self) -> None:
        """
        Verifica e divide o arquivo CSV se o limite de caracteres for excedido.

        Raises:
            FileNotFoundError: Se o arquivo CSV não existir.
        """
        if not os.path.exists(self.caminho_arquivo):
            raise FileNotFoundError(
                f"O arquivo CSV '{self.caminho_arquivo}' não existe."
            )

        nome_arquivo_base = os.path.splitext(os.path.basename(self.caminho_arquivo))[0]

        if not os.path.exists(self.pasta_saida):
            os.makedirs(self.pasta_saida)

        pasta_arquivo = os.path.join(self.pasta_saida, self.nome_arquivo)
        if not os.path.exists(pasta_arquivo):
            os.makedirs(pasta_arquivo)

        # Remover os arquivos existentes na pasta de saída
        arquivos_existentes = glob.glob(os.path.join(pasta_arquivo, "*.csv"))
        for arquivo in arquivos_existentes:
            os.remove(arquivo)

        if self.contar_linhas_csv() > self.num_linhas:
            self.dividir_texto_pandas(nome_arquivo_base, pasta_arquivo)
        else:
            self.dividir_texto_csv(nome_arquivo_base, pasta_arquivo)

    def contar_linhas_csv(self) -> int:
        """
        Conta o número de linhas no arquivo CSV.

        Returns:
            int: O número de linhas no arquivo CSV.
        """
        with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo_csv:
            total_linhas = sum(1 for linha in arquivo_csv)
        return total_linhas

    def dividir_texto_csv(self, nome_arquivo_base: str, pasta_arquivo: str) -> None:
        """
        Divide o texto em um arquivo CSV.

        Args:
            nome_arquivo_base (str): O nome base do arquivo CSV.
            pasta_arquivo (str): O diretório onde o arquivo CSV processado
                                 será armazenado.
        """
        with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            cabecalho = next(leitor_csv)
            coluna_indice = cabecalho.index(self.nome_coluna)
            for indice_linha, linha in enumerate(leitor_csv):
                if indice_linha >= self.num_linhas:
                    break
                texto = linha[coluna_indice]
                subtextos = self.dividir_texto_em_subtextos(texto)
                for indice_subtexto, subtexto in enumerate(subtextos):
                    nome_arquivo = os.path.join(
                        pasta_arquivo,
                        f"{nome_arquivo_base}_parte_{indice_linha + 1}_"
                        f"{indice_subtexto + 1}.csv",
                    )
                    with open(
                        nome_arquivo, "w", encoding="utf-8", newline=""
                    ) as arquivo_saida:
                        escritor_csv = csv.writer(arquivo_saida)
                        escritor_csv.writerow([self.nome_coluna])
                        escritor_csv.writerow([subtexto])
                self.monitorar_progresso(indice_linha, self.num_linhas)

    def dividir_texto_pandas(self, nome_arquivo_base: str, pasta_arquivo: str) -> None:
        """
        Divide o texto em um arquivo CSV usando pandas.

        Args:
            nome_arquivo_base (str): O nome base do arquivo CSV.
            pasta_arquivo (str): O diretório onde o arquivo CSV
                                 processado será armazenado.
        """
        data_frame = pd.read_csv(
            self.caminho_arquivo, engine="python", nrows=self.num_linhas
        )
        coluna_interesse = data_frame[self.nome_coluna]
        for indice_linha, texto in enumerate(coluna_interesse):
            subtextos = self.dividir_texto_em_subtextos(texto)
            for indice_subtexto, subtexto in enumerate(subtextos):
                nome_arquivo = os.path.join(
                    pasta_arquivo,
                    f"{nome_arquivo_base}_parte_{indice_linha + 1}_"
                    f"{indice_subtexto + 1}.csv",
                )
                data_frame_temporario = pd.DataFrame({self.nome_coluna: [subtexto]})
                data_frame_temporario.to_csv(nome_arquivo, index=False)
            self.monitorar_progresso(indice_linha, self.num_linhas)

    @staticmethod
    def dividir_texto_em_subtextos(texto: str, limite_tamanho: int = 5000) -> List[str]:
        """
        Divide o texto em subtextos.

        Args:
            texto (str): O texto a ser dividido.
            limite_tamanho (int, optional):
                O limite de tamanho para a divisão do texto.
            Defaults to 5000.

        Returns:
            List[str]: A lista de subtextos.
        """
        palavras = texto.split()
        subtextos = []
        subtexto_atual = ""
        for palavra in palavras:
            if len(subtexto_atual) + len(palavra) > limite_tamanho:
                subtextos.append(subtexto_atual.strip())
                subtexto_atual = ""
            subtexto_atual += palavra + " "
        if subtexto_atual:
            subtextos.append(subtexto_atual.strip())
        return subtextos

    @staticmethod
    def monitorar_progresso(linha_atual: int, total_linhas: int) -> None:
        """
        Monitora o progresso da divisão do arquivo.

        Args:
            linha_atual (int): O número da linha atual.
            total_linhas (int): O total de linhas no arquivo.
        """
        percentual = (linha_atual / total_linhas) * 100
        if percentual % 5 == 0:
            logging.info("Progresso: %s%% concluído", percentual)


if __name__ == "__main__":
    # O usuário será solicitado a fornecer informações sobre o arquivo CSV e as
    # configurações desejadas.
    caminho_arquivo_original = input("Digite o caminho do arquivo CSV: ")
    nome_coluna_interesse = input("Digite o nome da coluna que contém o texto: ")
    tamanho_maximo_caracteres = int(
        input("Digite o tamanho máximo de caracteres para cada subtexto: ")
    )
    num_linhas_leitura = int(input("Digite o número máximo de linhas a serem lidas: "))
    pasta_saida_final = input(
        "Digite o diretório onde os arquivos CSV divididos serão salvos: "
    )
    nome_arquivo_final = input("Digite o nome base para os arquivos CSV divididos: ")

    processador = CSVProcessor(
        caminho_arquivo_original,
        nome_coluna_interesse,
        tamanho_maximo_caracteres,
        num_linhas_leitura,
        pasta_saida_final,
        nome_arquivo_final,
    )
    processador.verificar_e_dividir_limite_caracteres_csv()
