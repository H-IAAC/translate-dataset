"""M2M100 Module."""

import logging

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

logger = logging.getLogger(__name__)


class M2m100Model:
    """M2M100 Class."""

    def __init__(self) -> None:
        """Init."""
        self.model = M2M100ForConditionalGeneration.from_pretrained(
            "facebook/m2m100_418M"
        )
        self.tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

    def translate_text(self, sentence):
        """Translate text."""
        # if count == text_limit: break

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
        return sentence_decoded[0]
