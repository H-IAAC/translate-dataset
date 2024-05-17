"""
Módulo para o modelo Nlbb.

Este módulo contém a implementação da classe NlbbModel, que utiliza o modelo M2M100 da biblioteca transformers para tradução de texto.
"""

import logging

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

logger = logging.getLogger(__name__)


class NlbbModel:
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
        self.model = M2M100ForConditionalGeneration.from_pretrained(
            "facebook/m2m100_418M"
        )
        self.tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

    def translate_text(self, sentence):
        """
        Traduz uma sentença do inglês para o português.

        Parâmetros:
        - sentence (str): A sentença em inglês a ser traduzida.

        Retorna:
        - list: Uma lista contendo a sentença traduzida em português.
        """
        list_of_sentences = []

        self.tokenizer.src_lang = "en"

        inputs = self.tokenizer(sentence, return_tensors="pt", padding=True)

        output_sequences = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            do_sample=False,  # test if batching affects output
            forced_bos_token_id=self.tokenizer.get_lang_id("pt"),
        )

        sentence_decoded = self.tokenizer.batch_decode(
            output_sequences, skip_special_tokens=True
        )
        list_of_sentences.append(sentence_decoded)
        return list_of_sentences
