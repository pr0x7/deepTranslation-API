from models import TranslationModel
from transformers import T5ForConditionalGeneration, T5Tokenizer

# can use t5-base t5-large, for complex operations , we using t5-small cos it is faster
tokenizer = T5Tokenizer.from_pretrained('t5-small', model_max_length=512)
translator = T5ForConditionalGeneration.from_pretrained('t5-small')


# store translation request in db

def store_translation(t):
    model = TranslationModel(base_lang=t.base_lang, text=t.text, target_lang=t.final_lang)
    model.save()
    return model.id


# run translation
# run a pretrained deep learning model
def run_translation(t_id: int):
    model = TranslationModel.get_by_id(t_id)
    prefix = f"translate {model.base_lang} to {model.target_lang}: {model.text}"
    input_ids = tokenizer(prefix, return_tensors='pt').input_ids
    outputs = translator.generate(input_ids, max_new_tokens=512)
    translation = tokenizer.decode(outputs[0], skip_speacial_tokens=True)
    model.translated_text = translation
    model.save()


# find the translation
# Retrieve the translation from the db

# return the translation
def find_translation(t_id: int):
    model = TranslationModel.get_by_id(t_id)
    translated_text = model.translated_text
    if translated_text is None:
        translated_text = "Processing..., check back in a minute"
    return {"translated_text": model.translated_text}
