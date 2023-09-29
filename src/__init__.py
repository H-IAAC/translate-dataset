from typing import List
from models.marian import MarianModel
from models.mbart import MbartModel
from models.t5 import t5Model
from models.nlbb import NlbbModel
from models.mbart import MbartModel
from utilities.check_csv_restricoes import verificar_restricoes_csv
import logging
import pandas as pd
from tqdm import tqdm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def select_model(modelname):
    if modelname == "marian":
        return MarianModel()
    elif modelname == "t5":
        return t5Model()
    elif modelname == "nlbb":
        return NlbbModel()
    elif modelname == "mbart":
        return MbartModel()
    logger.debug("Provided invalid modelname!")
        
def translate_csv(csv_path , collumns: List[str], models : List[str], output_format = "csv", filename=None):
    '''
    Args:
    csv_file (str): Path to the CSV file.
    columns_to_translate (list): List of column names to be translated.
    translation_map (dict): Dictionary containing the translation map for each column.

    '''
    verificar_restricoes_csv(csv_path)
    for modelname in models:
        logger.info(f"Initializing {modelname} model ...")        
        model = select_model(modelname)
        logger.info(f"Initializing {modelname} model ... done")        
        dataframe = pd.read_csv(csv_path)
        dataframe = dataframe[:10]
        for collum in collumns:
            translations = []
            for index, row in tqdm(dataframe.iterrows(), desc=f"Translating {collum} with {modelname}"):
                text = row[collum]
                translated_text = model.translate_text(text)
                translations.append(translated_text)
            translated_collum_name = f"{collum} {modelname} translation"
            dataframe[translated_collum_name] = translations
    
    dataframe.to_csv(f"{filename}_translation.csv")
            
def translate_webdataset(url, models : List[str]):
    pass

if __name__ == "__main__":

    # Configuração dos parâmetros de tradução
    #caminho_pasta_entrada_original = input("Digite o caminho da pasta de arquivo CSV: ")
    #caminho_pasta_saida_traduzida = input(
    #    "Digite o caminho do destino do arquivo CSV traduzido: "
    #)
    translate_csv("PATH TO FILE HERE", collumns=[" Category"," Question"], models=[ "marian"], filename="jeopardy")
