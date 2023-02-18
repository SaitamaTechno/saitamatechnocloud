import sql1
import docker
import threading
import datetime
from sys import exit
import dogecoin_testnet as doge
import time

#name_list=docker.get_names()
#size_list=docker.get_sizes()
#
#for i in range(len(name_list)):
#    print(name_list[i], size_list[i])
#exit()
def delete_docker(cname):
    docker.delete_docker(cname)
def get_date():
    date=datetime.datetime.now()
    year, month, day, hour=date.year, date.month, date.day, date.hour
    return [year, month, day, hour]
print("Started!")
mycount=0
while 1:
    try:
        for i in sql1.get_data_pc():
            #print(i)
            today=get_date()
            name=i[1]
            if i[5]=="active":
                size=docker.get_size_from_name(name)
                if size[-2]=="G":
                    size=float(size.replace("GB", ""))
                    #print(size)
                    if size>i[3]:
                        #print("deleted", name)
                        threading.Thread(target=delete_docker, args=(name,)).start()
                        sql1.delete_user_pc(name)
            first_day=i[6]
            #print(first_day)
            first_day_list=[int(a) for a in first_day.split("/")]
            print("First_day=", first_day_list)
            print("Today=", today)
            info=doge.get_wallet_info(i[0])
            available_balance=float(info["available_balance"])
            if first_day_list[0]==today[0] and today[1]==first_day_list[1] and first_day_list[2]==today[2] and first_day_list[3]+1==today[3] and i[5]=="active":
                #Code for payment
                if available_balance > i[4]:
                    threading.Thread(target=doge.send_money, args=(str(i[4]), i[0], "default",)).start()
                    new_date = str(today[0])+"/"+str(today[1])+"/"+str(today[2])+"/"+str(today[3])
                    sql1.update_date(i[1], new_date)
                    print("I got a payment.")
                else:
                    sql1.update_status(i[1], "passive")
                    docker.con_stop(i[1])
            elif first_day_list[0]==today[0] and today[1]==first_day_list[1] and first_day_list[2]==today[2] and first_day_list[3]+1+2==today[3] and i[5]=="passive":
                if available_balance > i[4]:
                    threading.Thread(target=doge.send_money, args=(str(i[4]), i[0], "default",)).start()
                    new_date = str(today[0])+"/"+str(today[1])+"/"+str(today[2])+"/"+str(today[3])
                    sql1.update_date(i[1], new_date)
                    sql1.update_status(i[1], "active")
                    docker.con_restart(i[1])
                    print("Passive turned active")
                else:
                    threading.Thread(target=delete_docker, args=(i[1],)).start()
                    sql1.delete_user_pc(i[1])
                    print("Computer deleted because of no money in wallet.")
    except TypeError:
        print("TypeError")
    mycount+=1
    print(mycount)
    time.sleep(60)
