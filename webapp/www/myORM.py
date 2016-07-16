#myORM.py
import aiomysql
import asyncio, os, json, time


#全局变量__pool存储
@asyncio.coroutine
def create_pool(loop, **kw):
	logging.info('create database connection pool...')
	global __pool
	__pool = yield from aiomysql.create_pool(
	host = kw.get('host', 'localhost'),
	port = kw.get('port', 3306),
	user = kw['user'],
	password = kw['password'],
	db = kw['db'],
	charset = kw.get('charset', 'utf-8'),
	autocommit = kw.get('autocommit', True)
	maxsize = kw.get('maxsize', 10),
	minsize = kw.get('minsize', 1),
	loop = loop
	)

#select函数传入sql语句和sql参数
@asyncio.coroutine
def select(sql, args, size = None):
	log(sql, args)
	global __pool
	with (yield from __pool) as conn:
		cur = yield from conn.cursor(aiomysql.DictCursor)
		yield from cur.execute(sql.replace('?', '%'), args or ())
		#如果传入size参数，就通过fetchmany()获取最多指定数量的记录
		#否则，通过fetchall()获取所有记录
		if size:
			rs = yield from cur.fetchmany(size)
		else:
			rs = yield from cur.fetchall()
		yield from cur.close()
		logging.info('rows returned: %s' % len(rs))
		return rs

#Insert, Update, Delete函数执行都需要相同的参数，定义一个通用的execute函数
@asyncio.coroutine
def execute(sql, args):
	log(sql)
	with (yield from __pool) as conn:
		try:
			cur = yield from conn.cursor()
			yield from cur.execute(sql.replace('?', '%'), args)
			affected = cur.rowcount()
			yield from cur.close()
		except BaseException as e:
			raise
		return affected

#？？？？？？？
def create_args_string(num):
	L = []
	for n in range(num)
		L.append('?')
	return ','.join(L)
	
#Field类，读取数据库字段
class Field(object):
	def __init__(self, name, column_type, primary_key, default)
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default
	
	def __str__(self):
		return '<%s, %s : %s>' % (self.__class__.__name__, self.column_type, self.name)
class StringField(Field):
	def __init__(self, name = None, primary_key = Falsem, default = None, ddl = 'varchar(100)'):
		super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):
	def __init__(self, name = None, default = False):
		super().__init__(name, 'boolean', False, default)

class IntegerField(Field):
	def __init__(self, name = None, primary_key = False, default = 0)
		super().__init__(name, 'bigint', primary_key, default)
		
class FloatField(Field):
	def __init__(self, name = None, primary_key = False, default = 0.0)
		super().__init__(name, 'real', primary_key, default)

class TextField(Field):
	def __init__(self, name = None, default = None):
		super().__init__(name, 'text', False, default)
			
		
			

	