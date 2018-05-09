from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase("data.db")

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):

    name = CharField(unique=True)
    join_date = DateTimeField()
    password = CharField()

class Item(BaseModel):

    name = CharField(unique=True)
    add_date = DateTimeField()
    days_available = IntegerField()
    description = TextField()

class FieldType(BaseModel):
    name = CharField()

class Field(BaseModel):

    field_type = ForeignKeyField(FieldType, backref="fields")
    item = ForeignKeyField(Item, backref="fields")
    data = TextField()
    image_link = CharField()

class Response(BaseModel):
    
    field = ForeignKeyField(Field, backref="responses")
    data = TextField()
