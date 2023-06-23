import sys
import logging
import csv


def verificar_restricoes_csv(caminho_arquivo: str) -> None:
    """
    Verifica as restrições de um arquivo CSV.

    Args:
        caminho_arquivo: O caminho para o arquivo CSV.

    Returns:
        None

    Raises:
        FileNotFoundError: Se o arquivo especificado não for encontrado.
        UnicodeDecodeError: Se ocorrer um erro de decodificação do arquivo CSV.
        csv.Error: Se ocorrer um erro relacionado à leitura do arquivo CSV.
    """
    # Configurar o logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Configurar o handler para imprimir os logs no console
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)

            # Verificar se o arquivo está vazio
            if not any(leitor_csv):
                logger.info("O arquivo CSV está vazio.")
                return

            # Verificar se o arquivo possui uma linha de cabeçalho
            cabecalho = next(leitor_csv, None)
            if not cabecalho:
                logger.info("O arquivo CSV não possui uma linha de cabeçalho.")
                return

            # Verificar o número de colunas
            numero_colunas = len(cabecalho)
            if numero_colunas < 2:
                logger.info("O arquivo CSV deve ter pelo menos duas colunas.")
                return

            # Verificar o conteúdo das colunas
            for linha in leitor_csv:
                if len(linha) != numero_colunas:
                    logger.info("O arquivo CSV possui linhas com números de colunas diferentes.")
                    return

    except FileNotFoundError:
        logger.exception(f"O arquivo CSV '{caminho_arquivo}' não foi encontrado.")
        raise

    except UnicodeDecodeError:
        logger.exception(f"Erro de decodificação do arquivo CSV '{caminho_arquivo}'.")
        raise

    except csv.Error:
        logger.exception(f"Erro durante a leitura do arquivo CSV '{caminho_arquivo}'.")
        raise

    logger.info("O arquivo CSV atende a todas as restrições.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python verificar_restricoes_csv.py caminho_arquivo")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]
    verificar_restricoes_csv(caminho_arquivo)