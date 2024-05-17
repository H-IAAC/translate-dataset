"""NLLB module."""

import logging

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

source_lang = "eng_Latn"
target_lang = "por_Latn"

logger = logging.getLogger(__name__)


class NllbModel:
    """
    Classe para o modelo Nlbb.

    Esta classe utiliza o modelo M2M100 da biblioteca transformers para
    traduzir texto do inglês para o português.

    Métodos:
    - __init__: Inicializa o modelo e o tokenizador.
    - translate_text: Traduz uma sentença do inglês para o português.
    """

    def __init__(self) -> None:
        """
        Inicializa uma nova instância do modelo Nlbb.

        O modelo e o tokenizador M2M100 são carregados a partir dos recursos
        predefinidos do Facebook.
        """
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            "facebook/nllb-200-distilled-600M"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            "facebook/nllb-200-distilled-600M"
        )
        self.translator = pipeline(
            "translation",
            model=self.model,
            tokenizer=self.tokenizer,
            src_lang=source_lang,
            tgt_lang=target_lang,
            max_length=400,
        )

    def translate_text(self, sentence):
        """
        Traduz uma sentença do inglês para o português.

        Parâmetros:
        - sentence (str): A sentença em inglês a ser traduzida.

        Retorna:
        - list: Uma lista contendo a sentença traduzida em português.
        """
        out = self.translator(sentence)
        out = [o["translation_text"] for o in out]
        return out[0]
