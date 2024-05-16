"""Módulo de testes unitários."""

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utilities.break_text import CSVProcessor

# Adiciona a pasta raiz ao PYTHONPATH.


def test_verificar_e_dividir_limite_caracteres_csv_raises_file_not_found_error():
    """Testa se a função levanta um FileNotFoundError quando o arquivo não é encontrado."""
    processador = CSVProcessor(
        "caminho/nao/existente.csv",
        "coluna",
        500,
        5,
        "data/raw/cnn_dailymail",
        "train.csv",
    )
    with pytest.raises(FileNotFoundError):
        processador.verificar_e_dividir_limite_caracteres_csv()


def test_contar_linhas_csv():
    """Testa a função contar_linhas_csv."""
    processador = CSVProcessor(
        "/home/sildolfoneto/Documents/translate-dataset/translate_dataset/data/raw/cnn_dailymail/train.csv",
        "article",
        500,
        1088106,
        "data/interim",
        "test_train",
    )
    num_linhas = processador.contar_linhas_csv()
    assert num_linhas == 1088106  # Substitua 1088106 pelo número esperado de linhas.


def test_dividir_texto_csv():
    """Testa a função dividir_texto_csv."""
    processador = CSVProcessor(
        "/home/sildolfoneto/Documents/translate-dataset/translate_dataset/data/raw/cnn_dailymail/train.csv",
        "article",
        500,
        5,
        "/home/sildolfoneto/Documents/translate-dataset/translate_dataset/data/interim",
        "test_train_dividi_texto",
    )
    processador.verificar_e_dividir_limite_caracteres_csv()
    assert os.path.exists(
        "/home/sildolfoneto/Documents/translate-dataset/translate_dataset/data/raw/cnn_dailymail/train.csv"
    )


def test_dividir_texto_pandas():
    """Testa a função dividir_texto_pandas."""
    processador = CSVProcessor(
        "/home/sildolfoneto/Documents/translate-dataset/translate_dataset/data/raw/cnn_dailymail/train.csv",
        "article",
        500,
        5,
        "/home/sildolfoneto/Documents/translate-dataset/translate_dataset/data/interim",
        "test_train",
    )
    processador.verificar_e_dividir_limite_caracteres_csv()
    assert os.path.exists(
        "/home/sildolfoneto/Documents/translate-dataset/translate_dataset/data/raw/\
        cnn_dailymail/train.csv"
    )


def test_dividir_texto_em_subtextos():
    """Testa a função dividir_texto_em_subtextos."""
    processador = CSVProcessor(
        "",
        "",
        500,
        0,
        "",
        "",
    )
    subtextos = processador.dividir_texto_em_subtextos(
        "texto com mais de dez caracteres", 10
    )
    assert len(subtextos) == 4  # O texto deveria ser dividido em três partes.
