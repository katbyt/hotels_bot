from peewee import SqliteDatabase, Model, IntegerField, CharField, DateTimeField, TextField
import datetime
import os

db = SqliteDatabase(os.path.join('database', 'hotels.db'))


class User(Model):
    user_id = IntegerField()
    command = CharField()
    created_date = DateTimeField(default=datetime.datetime.now)
    history = TextField()

    class Meta:
        database = db


with db:
    User.create_table()
