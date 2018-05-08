from peewee import *

db = SqliteDatabase("data.db")


class User(Model):

    name = CharField(unique=True)
    join_date = DateTimeField()
    password = CharField()

    class Meta:
        database = db

class Item(Model):

    name = CharField()
    add_date = DateTimeField()
    days_available = IntegerField()
    description = TextField()

class FieldType():
    name = CharField()

    class Meta:
        database = db

class Field():

    field_type = ForeignKeyField(FieldType, backref="fields")
    data = TextField()

    class Meta:
        database = db

class Response():
    
    field = ForeignKeyField(Field, backref="responses")
    data = TextField()

    class Meta:
        database = db