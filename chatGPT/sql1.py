import sqlite3
con = sqlite3.connect("data/userdata.db", check_same_thread=False)
cur = con.cursor()

#cur.execute("CREATE TABLE key_table (key, number)")
#cur.execute("CREATE TABLE pc_table (username, computer_name, hostports, disk_size, doge, status, date)")
#cur.execute("CREATE TABLE register (username, password, email, verification_code, verified)")
#res = cur.execute("SELECT name FROM sqlite_master")
#cur.execute("DELETE FROM pc_table")
#cur.execute("DELETE FROM register")
#print(res.fetchall())
def data_from_key(key):
	res = cur.execute(
	'''
	SELECT * FROM key_table WHERE key=?
	''', (key,))
	try:
		return res.fetchall()[0][1]
	except IndexError:
		return -1
def data_all_key():
	res = cur.execute(
	'''
	SELECT * FROM key_table
	''')
	return res.fetchall()
def update_key(key, number):
	cur.execute(
	'''
	UPDATE key_table SET number=? WHERE key=?
	''', [number, key])
	con.commit()
def create_key(key, number):
	cur.execute(
	'''
	INSERT INTO key_table (key, number)
	VALUES (?,?)
	''', [key, number])
	con.commit()
def data_from_computername_pc(computer_name):
	res = cur.execute(
	'''
	SELECT * FROM pc_table WHERE computer_name=?
	''', (computer_name,))
	return res.fetchall()
def data_from_username_pc(username):
	res = cur.execute(
	'''
	SELECT * FROM pc_table WHERE username=?
	''', (username,))
	return res.fetchall()
def update_date(computer_name, date):
	cur.execute(
	'''
	UPDATE pc_table SET date=? WHERE computer_name=?
	''', [date, computer_name])
	con.commit()
def update_status(computer_name, status):
	cur.execute(
	'''
	UPDATE pc_table SET status=? WHERE computer_name=?
	''', [status, computer_name])
	con.commit()
def delete_user_pc(computer_name):
	cur.execute(
	'''
	DELETE FROM pc_table WHERE computer_name=?
	''', (computer_name,)
	)
	con.commit()
def get_data_pc():
	res = cur.execute("SELECT * FROM pc_table")
	return res.fetchall()
def update_ports(computer_name, ports):
	cur.execute(
	'''
	UPDATE pc_table SET hostports=? WHERE computer_name=?
	''', [ports, computer_name])
	con.commit()
def create_pc(username, computer_name, disk_size, doge, status, date):
	cur.execute(
	'''
	INSERT INTO pc_table (username, computer_name, disk_size, doge, status, date)
	VALUES (?,?,?,?,?,?)
	''', [username, computer_name, disk_size, doge, status, date])
	con.commit()
def create_user(username, password, email, verification_code, verified):
	cur.execute(
	'''
	INSERT INTO register VALUES (?,?,?,?,?,?)
	''', [username, password, email, verification_code, verified, 190719071907])
	con.commit()
def change_password(username, newpassword):
	cur.execute(
	'''
	UPDATE register SET password=? WHERE username=?
	''', (newpassword, username)
	)
	con.commit()
def update_forgot_pass(username, forgot_pass):
	cur.execute(
	'''
	UPDATE register SET forgot_pass=? WHERE username=?
	''', (forgot_pass, username)
	)
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
def get_emails():
	res = cur.execute(
	'''
	SELECT email FROM register
	''')
	return res.fetchall()
def get_data():
	res = cur.execute("SELECT * FROM register")
	return res.fetchall()
def insert_column(col_name):
	res = cur.execute("ALTER TABLE register ADD {};".format(col_name))
	con.commit()
def delete_column(col_name):
	res = cur.execute("ALTER TABLE register DROP COLUMN {};".format(col_name))
	con.commit()
#cur.execute("DROP TABLE register")
#res = cur.execute("SELECT username FROM register")
#print(res.fetchall())
con.commit()
#create_user("enes", "asdas32", "asdsad€mail.com", 123456, 0)
