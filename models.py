from peewee import Model, SqliteDatabase, CharField, TextField

db = SqliteDatabase('translations.db')


class TranslationModel(Model):
    base_lang = CharField()
    text = TextField()
    target_lang = CharField()
    translated_text = TextField(null=True)

    class Meta:
        database = db


db.create_tables([TranslationModel])


