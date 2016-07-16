#myUser.py

from myORM import Model, StringField, IntegerField

class User():
	__table__ == '__users__'
	
	id = IntegerField(primary_key = True)
	name = StringField()