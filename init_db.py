from models import *
import datetime

db.connect()

db.create_tables([User, Item, FieldType, Field, Response])


User.create_table()
Item.create_table()
FieldType.create_table()
Field.create_table()
Response.create_table()


u = User.create(name="TAN", join_date=datetime.datetime.now(), password="abc")
u.save()

u = User.create(name="CIT", join_date=datetime.datetime.now(), password="123")
u.save()

for item in ["intrebare", "combobox", "select", "checkbox"]:
    f = FieldType.create(name=item)
    f.save()


db.close()