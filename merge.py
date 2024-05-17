"""Merge module."""

import csv
import logging
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def merge_csv_files(directory_path, output_file):
    """
    Combina diferentes arquivos .csv em 1 só.

    O script une os arquivos CSV que
    possuem um padrão de nome "nome_parte_X_Y.csv", onde X é o mesmo
    para diferentes partes e Y varia, em uma única linha no novo arquivo CSV.

    Args:
        directory_path (str): O caminho do diretório contendo os arquivos CSV
        separados.
        output_file (str): O caminho do arquivo de saída que será gerado.
    """
    merged_data = []
    current_row = []
    header = None

    for filename in sorted(os.listdir(directory_path)):
        if filename.endswith(".csv"):
            with open(os.path.join(directory_path, filename), "r", newline="") as file:
                reader = csv.reader(file)
                rows = list(reader)
                if header is None:
                    header = rows[0]
                if len(rows) == 1:
                    current_row.extend(rows[0])
                elif (
                    len(rows) >= 2 and filename.endswith("_1.csv") and len(rows[1]) >= 1
                ):
                    if current_row:
                        merged_data.append(current_row)
                    current_row = rows[1]
                elif (
                    len(rows) >= 2 and filename.endswith("_2.csv") and len(rows[1]) >= 1
                ):
                    current_row.extend(rows[1])

    if current_row:
        merged_data.append(current_row)

    merged_data.insert(0, header)

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(merged_data)

    logging.info("Arquivo CSV merged gerado: %s", output_file)


if __name__ == "__main__":
    # Configuração dos parâmetros
    directory_path = input(
        "Digite o caminho do diretório contendo os arquivos CSV separados: "
    )
    output_file = input("Digite o caminho do arquivo CSV de saída que será gerado: ")

    # Execução do merge
    merge_csv_files(directory_path, output_file)
    print("Hello!")
