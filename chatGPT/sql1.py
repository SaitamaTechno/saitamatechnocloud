import sqlite3
con = sqlite3.connect("data/userdata.db", check_same_thread=False)
cur = con.cursor()
#cur.execute("CREATE TABLE register (username, password, email, verification_code, verified)")
#res = cur.execute("SELECT name FROM sqlite_master")
#print(res.fetchall())
def create_user(username, password, email, verification_code, verified):
	cur.execute(
	'''
	INSERT INTO register VALUES (?,?,?,?,?)
	''', [username, password, email, verification_code, verified])
	con.commit()
def update_code(username, verification_code):
	cur.execute(
	'''
	UPDATE register SET verification_code=? WHERE username=?
	''', (verification_code, username)
	)
	con.commit()
def update_verified(username, verified):
	cur.execute(
	'''
	UPDATE register SET verified=? WHERE username=?
	''', (verified, username)
	)
	con.commit()
def delete_user(username):
	cur.execute(
	'''
	DELETE FROM register WHERE username=?
	''', (username,)
	)
	con.commit()
def data_from_username(username):
	res = cur.execute(
	'''
	SELECT * FROM register WHERE username=?
	''', (username,))
	return res.fetchall()
def get_usernames():
	res = cur.execute(
	'''
	SELECT username FROM register
	''')
	return res.fetchall()
def get_data():
	res = cur.execute("SELECT * FROM register")
	return res.fetchall()
#cur.execute("DROP TABLE register")
#res = cur.execute("SELECT username FROM register")
#print(res.fetchall())
con.commit()
#create_user("enes", "asdas32", "asdsad€mail.com", 123456, 0)
