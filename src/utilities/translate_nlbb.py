from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


# This model requires transformers==4.31.0
# it needs 

model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")


def traduzir_m2m100(sentence):
    list_of_sentences = []

    tokenizer.src_lang = "en"

    inputs = tokenizer(sentence, return_tensors="pt", padding=True)

    output_sequences = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        do_sample=False,  # disable sampling to test if batching affects output
            forced_bos_token_id=tokenizer.get_lang_id("pt")
    )

    sentence_decoded = tokenizer.batch_decode(output_sequences, skip_special_tokens=True)
    list_of_sentences.append(sentence_decoded)
    return list_of_sentences
    
if __name__ == "__main__":
    
    sentences = ['A woman talks nearby as water pours', 'Multiple clanging and clanking sounds', 'The wind is blowing, insects are singing, and rustling occurs', 'The wind is blowing and rustling occurs', 'Person is whistling', 'A motorboat cruises along, and a man talks', 'The sizzling of food while a dish is clanking', 'Someone has a hiccup while typing', 'Aircraft engine hum with man and woman speaking', 'Hissing followed by clanking dishes and speech']
    for s in sentences:
        print(traduzir_m2m100(s))