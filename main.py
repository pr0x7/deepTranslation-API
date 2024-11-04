from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, validator
import tasks

app = FastAPI()

languages = ["English", "French", "Spanish", "German", "Italian", "Portuguese", "Russian", "Japanese", "Korean",
             "Chinese", "Romanian"]


class Translation(BaseModel):
    text: str
    base_lang: str
    final_lang: str

    @validator('base_lang', 'final_lang')
    def valid_length(cls, lang):
        if lang not in languages:
            raise ValueError('Language not supported')
        return lang


# Route 1:/
# Test if everything is working
# {'message': 'Hello World!'}
@app.get("/")
def get_root():
    return {"message": "Hello World!"}


# Route 2:/translate
# Take in a translation request with a JSON body, store it in db and return the translated text[ID]
@app.post("/translate")
def post_translate(translation: Translation, background_tasks: BackgroundTasks):
    t_id = tasks.store_translation(translation)
    background_tasks.add_task(tasks.run_translation, t_id)
    return {"id": t_id}


# Route 3:/results
# Take in a translation ID and return the translated text
@app.get("/results/{t_id}")
def get_results(t_id: int):
    model = tasks.TranslationModel.get_by_id(t_id)
    return {"translation": model.translated_text}
