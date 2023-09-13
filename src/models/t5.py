import pandas as pd
from transformers import (AutoModelForSeq2SeqLM, AutoTokenizer,
                          T5ForConditionalGeneration, T5Tokenizer)
import logging


class t5Model():
    def __init__(self) -> None:
        
        model_name = "unicamp-dl/translation-en-pt-t5"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    def traduzir_t5(self, sentence):
        """
        Translates the input sentence.

        Args:
            sentence (str): The input sentence to be translated.

        Returns:
            str: The translated version of the input sentence.
        """
        task_prefix = "translate English to Portuguese:"
        inputs = self.tokenizer(task_prefix + sentence, return_tensors="pt", padding=True)

        output_sequences = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            do_sample=False,  # disable sampling to test if batching affects output
        )
        sentence_decoded = self.tokenizer.batch_decode(
            output_sequences, skip_special_tokens=True
        )

        return sentence_decoded
