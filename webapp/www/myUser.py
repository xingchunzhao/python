#myUser.py

import myORM
from myModel import User, Blog, Comment
import asyncio, aiomysql
import sys

#class User():
	#__table__ == '__users__'
	
	#id = IntegerField(primary_key = True)
	#name = StringField()


def test(loop):
	yield from myORM.create_pool(loop = loop, host = '127.0.0.1', port = '3306', user = 'www-data', password = 'www-data', db = 'mypython')
	u = User(name = 'Test', email = 'test@example.com', password = '1234567890', image = 'about:block' )
	
	yield from u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
if loop.is_closed():
	sys.exit()

	
#for x in test():
#	pass
	