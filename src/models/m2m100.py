import logging

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

logger = logging.getLogger(__name__)


class MarianModel:
    def __init__(self) -> None:
        self.model = M2M100ForConditionalGeneration.from_pretrained(
            "facebook/m2m100_418M"
        )
        self.tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

    def translate_text(self, sentence):
        # if count == text_limit: break

        inputs = self.tokenizer(sentence, return_tensors="pt", padding=True)

        output_sequences = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            do_sample=False,  # disable sampling to test if batching affects output
            forced_bos_token_id=self.tokenizer.get_lang_id("pt"),
        )

        sentence_decoded = self.tokenizer.batch_decode(
            output_sequences, skip_special_tokens=True
        )
        return sentence_decoded
