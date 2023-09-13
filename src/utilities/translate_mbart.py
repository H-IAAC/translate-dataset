from transformers import MBart50TokenizerFast, MBartForConditionalGeneration

tokenizer = MBart50TokenizerFast.from_pretrained('Narrativa/mbart-large-50-finetuned-opus-en-pt-translation')
model = MBartForConditionalGeneration.from_pretrained('Narrativa/mbart-large-50-finetuned-opus-en-pt-translation')

def translate_mbart(sentence):
    tokenizer.src_lang = 'en_XX'

    inputs = tokenizer(sentence , return_tensors="pt", padding=True)

    output_sequences = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        do_sample=False,  # disable sampling to test if batching affects output
        forced_bos_token_id=tokenizer.lang_code_to_id['pt_XX']
    )

    sentence_decoded = tokenizer.batch_decode(output_sequences, skip_special_tokens=True)
    return sentence_decoded

if __name__ == "__main__":
    
    sentences = ['A woman talks nearby as water pours', 'Multiple clanging and clanking sounds', 'The wind is blowing, insects are singing, and rustling occurs', 'The wind is blowing and rustling occurs', 'Person is whistling', 'A motorboat cruises along, and a man talks', 'The sizzling of food while a dish is clanking', 'Someone has a hiccup while typing', 'Aircraft engine hum with man and woman speaking', 'Hissing followed by clanking dishes and speech']
    for s in sentences:
        print(translate_mbart(s))