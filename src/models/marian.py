"""Marian module."""

import logging

from transformers import MarianMTModel, MarianTokenizer

logger = logging.getLogger(__name__)


class MarianModel:
    """Marian Model Class."""

    def __init__(self) -> None:
        """Init function."""
        model_name = "Helsinki-NLP/opus-mt-en-ROMANCE"
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)

    def translate_text(self, sentence):
        """Translate text."""
        inputs = self.tokenizer(
            ">>pt<<" + sentence if len(sentence) < 512 else ">>pt<<" + sentence[:512],
            return_tensors="pt",
            padding=True,
        )

        output_sequences = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            do_sample=False,  # test if batching affects output,
            max_length=1024,
        )
        sentence_decoded = self.tokenizer.batch_decode(
            output_sequences, skip_special_tokens=True
        )

        return sentence_decoded[0]
