from typing import List
from models.marian import MarianModel
from models.mbart import MbartModel
from models.t5 import t5Model
from utilities.check_csv_restricoes import verificar_restricoes_csv
import logging
import pandas as pd

model_dict = { "marian" : MarianModel(),
                "mbart" : MbartModel(),
                #"t5" : t5Model()
    
}
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def translate_csv(csv_file , collumns: str, models : List[str], output_format = "csv"):
    '''
    Args:
    csv_file (str): Path to the CSV file.
    columns_to_translate (list): List of column names to be translated.
    translation_map (dict): Dictionary containing the translation map for each column.

    '''
    verificar_restricoes_csv(csv_file)
    for modelname in models:
        logger.info(f"Initializing {modelname} model ...")        
        model = model_dict[modelname]
        logger.info(f"Initializing {modelname} model ... done")        
    
    
def translate_webdataset():
    pass

if __name__ == "__main__":

    # Configuração dos parâmetros de tradução
    #caminho_pasta_entrada_original = input("Digite o caminho da pasta de arquivo CSV: ")
    #caminho_pasta_saida_traduzida = input(
    #    "Digite o caminho do destino do arquivo CSV traduzido: "
    #)
    translate_csv("/home/guilhermeramirez/nlp/translate-dataset/data/raw/test.csv","article", models=["marian"])
