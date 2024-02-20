import sqlite3

database:str = "mystudentdb.db"

def connect():
	return sqlite3.connect(database)

def getprocess(sql:str)->list:
	conn = connect()
	conn.row_factory = sqlite3.Row # to return a dictionary formatted data
	cursor = conn.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	cursor.close()
	return rows
	
def doprocess(sql:str)->bool:
	conn = connect()
	conn.row_factory = sqlite3.Row # to return a dictionary formatted data
	cursor = conn.cursor()
	cursor.execute(sql)
	conn.commit()
	cursor.close()
	return True if cursor.rowcount>0 else False
	
def deleterecord(table:str,**kwargs)->bool:
	sql:str = ""
	for key,value in kwargs.items():
		sql = f"DELETE FROM `{table}` WHERE `{key}` = '{value}'"
	return doprocess(sql)
	

def addrecord(table:str,**kwargs)->bool:
	keys:list = list(kwargs.keys())
	vals:list = list(kwargs.values())
	flds:str = "`,`".join(keys)		
	data:str = "','".join(vals)		
	sql:str = f"INSERT INTO `{table}`(`{flds}`) VALUES ('{data}')"
	return doprocess(sql)
	
def updaterecord(table:str,**kwargs)->bool:
	keys:list = list(kwargs.keys())
	vals:list = list(kwargs.values())
	flds:list = []
	for i in range(1,len(keys)):
		flds.append(f"`{keys[i]}`='{vals[i]}'")
	fld:str = ",".join(flds)
	sql:str = f"UPDATE `{table}` SET {fld} WHERE `{keys[0]}`='{vals[0]}'"
	print(sql)
	return doprocess(sql)
	
def getall(table:str)->list:
	sql:str = f"SELECT * FROM `{table}`"
	return getprocess(sql)
	
def userlogin(table:str,**kwargs)->bool:
	sql:str = ""
	for key,value in kwargs.items():
		sql = f"SELECT * FROM `{table}` WHERE `{key}` = '{value}'"
	return getprocess(sql)
	
	

def main()->None:
	rows = getall('student')
	for row in rows:
		print(dict(row))

if __name__=="__main__":
	main()
	