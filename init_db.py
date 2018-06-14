from models import *
import datetime
import os
import hashlib

if os.path.exists("data.db"):
    os.unlink("data.db")

def make_bytes(data):

    return bytes(data, "utf-8")
   
db.connect()

db.create_tables([User, Item, Question, Response])

print("creating tables")
User.create_table()
Item.create_table()
Question.create_table()
Response.create_table()
print("done")

u = User.create(name="TAN", join_date=datetime.datetime.now(), password=hashlib.md5(make_bytes("abc")).hexdigest())
u.save()

u = User.create(name="CIT", join_date=datetime.datetime.now(), password=hashlib.md5(make_bytes("123")).hexdigest())
u.save()

print("createed users")

db.close()

print("done")