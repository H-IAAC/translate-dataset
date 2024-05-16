import logging

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

source_lang = "eng_Latn"
target_lang = "por_Latn"

logger = logging.getLogger(__name__)


class NllbModel:
    def __init__(self) -> None:
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
        list_of_sentences = []
        out = self.translator(sentence)
        out = [o["translation_text"] for o in out]
        return out[0]
