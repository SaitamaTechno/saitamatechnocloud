import sql1
import datetime
#sql1.create_user("ali", "mypassword", "myemail@gmail.com", 123456, 0)
#sql1.update_code("enes", 999999)
#sql1.update_verified("ali", 1)
#sql1.update_forgot_pass(username, forgot_pass)
#sql1.delete_user("enes")
#print(sql1.data_from_username("enes"))
#print(sql1.get_usernames())
#print(sql1.get_emails())
#sql1.insert_column("forgot_pass")
#sql1.delete_column("forgot_pass")
def get_date():
    date=datetime.datetime.now()
    mystr=str(date.year)+"/"+ str(date.month)+ "/" + str(date.day)
    return mystr
#sql1.create_pc("enes", "mylinux", "1", 2, "active", get_date())
#sql1.update_ports("mylinux", str([12,13,14,15,16,17,18,19,20]))
#sql1.delete_user_pc("enesbabba")
#sql1.delete_user_pc("enes")


#data=sql1.data_from_username_pc("enes")[0]
#portlist=[int(i) for i in data[2].replace("[", "").replace("]", "").split(", ")]
#print(portlist)
#print(sql1.data_from_username_pc("saitama")[0])
#print(sql1.data_from_computername_pc("enes")[0])
#print(sql1.data_from_username("saitama")[0][2])
#for i in sql1.get_data_pc():
#    print(i)
#print(len(sql1.get_usernames()))
#if "enes" in [sql1.get_usernames()[i][i] for i in range(len(sql1.get_usernames())-1)]:
#	print("okay")

#sql1.create_key("SAITAMATECHNO5", 5)
#sql1.create_key("LINKEDIN2", 2)
#sql1.update_key("SAITAMATECHNO5", 5)
#sql1.update_key("LINKEDIN2", 2)

print(sql1.data_all_key())
#print(sql1.data_from_key("SAITAMATECHNO5"))