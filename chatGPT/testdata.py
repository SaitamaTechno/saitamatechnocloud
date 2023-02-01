import sql1

#sql1.create_user("ali", "mypassword", "myemail@gmail.com", 123456, 0)
#sql1.update_code("enes", 999999)
#sql1.update_verified("ali", 1)
#sql1.delete_user("enes")
#print(sql1.data_from_username("enes"))
#print(sql1.get_usernames())
for i in sql1.get_data():
	print(i)
#print(len(sql1.get_usernames()))
#if "enes" in [sql1.get_usernames()[i][i] for i in range(len(sql1.get_usernames())-1)]:
#	print("okay")
