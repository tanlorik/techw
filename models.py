from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase("data.db")

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):

    name = CharField(unique=True)
    join_date = DateTimeField(null=True)
    password = CharField()
    sid = CharField(null=True)

class Item(BaseModel):

    name = CharField(unique=True)
    add_date = DateTimeField(null=True)
    days_available = IntegerField(null=True)
    description = TextField(null=True)
    image_link = CharField(null=True)

class Question(BaseModel):

    item = ForeignKeyField(Item, backref="fields")
    qtype = IntegerField(null=True)
    data = TextField(null=True)
    name = CharField(null=True)

class Response(BaseModel):
    
    field = ForeignKeyField(Question, backref="responses")
    data = TextField(null=True)
