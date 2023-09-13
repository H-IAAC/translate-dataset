from transformers import MBart50TokenizerFast, MBartForConditionalGeneration




class MbartModel():
    def __init__(self) -> None:
        self.tokenizer = MBart50TokenizerFast.from_pretrained('Narrativa/mbart-large-50-finetuned-opus-en-pt-translation')
        self.model = MBartForConditionalGeneration.from_pretrained('Narrativa/mbart-large-50-finetuned-opus-en-pt-translation')
            
    def translate_mbart(self, sentence):
        self.tokenizer.src_lang = 'en_XX'

        inputs = self.tokenizer(sentence , return_tensors="pt", padding=True)

        output_sequences = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            do_sample=False,  # disable sampling to test if batching affects output
            forced_bos_token_id=self.tokenizer.lang_code_to_id['pt_XX']
        )

        sentence_decoded = self.tokenizer.batch_decode(output_sequences, skip_special_tokens=True)
        return sentence_decoded
