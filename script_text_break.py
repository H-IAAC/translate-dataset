import pandas as pd
import csv
import os
import glob
from google.cloud import translate_v2 as translate


raw_cnn_data = pd.read_csv('data/raw/cnn_dailymail/train.csv')

one_line = raw_cnn_data.iloc[0]



""" def verificar_restricoes_csv(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        
        # Verificar se o arquivo está vazio
        if not any(leitor_csv):
            print("O arquivo CSV está vazio.")
            return
        
        # Verificar se o arquivo possui uma linha de cabeçalho
        cabecalho = next(leitor_csv, None)
        if not cabecalho:
            print("O arquivo CSV não possui uma linha de cabeçalho.")
            return
        
        # Verificar o número de colunas
        numero_colunas = len(cabecalho)
        if numero_colunas < 2:
            print("O arquivo CSV deve ter pelo menos duas colunas.")
            return
        
        # Verificar o conteúdo das colunas
        for linha in leitor_csv:
            if len(linha) != numero_colunas:
                print("O arquivo CSV possui linhas com números de colunas diferentes.")
                return
    
    print("O arquivo CSV atende a todas as restrições.")
    
# Exemplo de uso
arquivo_csv = 'data/raw/cnn_dailymail/train.csv'  # Substitua pelo caminho real do seu arquivo CSV
verificar_restricoes_csv(arquivo_csv) """


""" def verificar_limite_caracteres_csv(caminho_arquivo, coluna_verificada):
    limite_caracteres = 5000
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.DictReader(arquivo_csv)
        for linha in leitor_csv:
            texto = linha[coluna_verificada]
            if len(texto) > limite_caracteres:
                return False
    return True

# Exemplo de uso
arquivo_csv = 'data/raw/cnn_dailymail/train.csv'   # Substitua pelo caminho real do seu arquivo CSV
coluna_verificada = 'article'  # Substitua pelo nome da coluna a ser verificada
if verificar_limite_caracteres_csv(arquivo_csv, coluna_verificada):
    print("O texto na coluna está dentro do limite de caracteres por chamada.")
else:
    print("O texto na coluna excede o limite de caracteres por chamada e precisa ser dividido.") """


def verificar_e_dividir_limite_caracteres_csv(caminho_arquivo, nome_coluna, tamanho_maximo, num_linhas):
    if not os.path.exists(caminho_arquivo):
        print(f"O arquivo CSV '{caminho_arquivo}' não existe.")
        return
    
    nome_arquivo_base = os.path.splitext(os.path.basename(caminho_arquivo))[0]
    pasta_saida = nome_arquivo_base + "_saida"

    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    else:
        # Remover os arquivos existentes na pasta de saída
        arquivos_existentes = glob.glob(os.path.join(pasta_saida, '*.csv'))
        for arquivo in arquivos_existentes:
            os.remove(arquivo)

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

                with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
                    escritor_csv = csv.writer(arquivo_csv)
                    escritor_csv.writerow([nome_coluna])
                    escritor_csv.writerow([subtexto])

                #print(f"Arquivo CSV gerado: {caminho_arquivo}")

            linha_atual += 1
            monitorar_progresso(linha_atual, total_linhas)

def dividir_texto_em_subtextos(texto, tamanho_maximo):
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

def monitorar_progresso(linha_atual, total_linhas):
    porcentagem_conclusao = (linha_atual / total_linhas) * 100
    print(f"Progresso: {linha_atual}/{total_linhas} linhas processadas ({porcentagem_conclusao:.4f}%)")

# Exemplo de uso
caminho_arquivo_csv = 'data/raw/cnn_dailymail/train.csv'  # Substitua pelo caminho real do seu arquivo CSV
nome_coluna_verificada = 'article'  # Substitua pelo nome da coluna a ser verificada
limite_caracteres = 4998
num_linhas = 15  # Número máximo de linhas a serem lidas

verificar_e_dividir_limite_caracteres_csv(caminho_arquivo_csv, nome_coluna_verificada, limite_caracteres, num_linhas)