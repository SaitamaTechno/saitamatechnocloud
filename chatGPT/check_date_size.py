# Makes monthly payments and checks each computer's size.

import sql1
import docker
import threading
import datetime
from sys import exit
import dogecoin_testnet as doge
import time
from smtpmail import sendmaill_msg
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
            username=i[0]
            email=sql1.data_from_username(username)[0][2]
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
                        threading.Thread(target=sendmaill_msg, args=(email, "Your computer is deleted because you overused your disk more than your disk size.",)).start()
            first_day=i[6]
            #print(first_day)
            first_day_list=[int(a) for a in first_day.split("/")]
            print("First_day=", first_day_list)
            print("Today=", today)
            info=doge.get_wallet_info(i[0])
            available_balance=float(info["available_balance"])
            if first_day_list[0]==today[0] and first_day_list[1]+1==today[1] and first_day_list[2]==today[2] and first_day_list[3]==today[3] and i[5]=="active":
                #Code for payment
                if available_balance > i[4]:
                    threading.Thread(target=doge.send_money, args=(str(i[4]), i[0], "default",)).start()
                    new_date = str(today[0])+"/"+str(today[1])+"/"+str(today[2])+"/"+str(today[3])
                    sql1.update_date(i[1], new_date)
                    #print("I got a payment.")
                    threading.Thread(target=sendmaill_msg, args=(email, "Your payment has been received: "+str(i[4])+" Doge",)).start()
                else:
                    sql1.update_status(i[1], "passive")
                    docker.con_stop(i[1])
                    until_date=str(today[0])+"/"+str(today[1])+"/"+str(today[2]+2)
                    threading.Thread(target=sendmaill_msg, args=(email, "Your computer has turned passive because you don't have enough money in your wallet. You can turn it active if you charge your wallet in 2 days (until "+until_date+"). Otherwise, It will be deleted!",)).start()
            elif first_day_list[0]==today[0] and first_day_list[1]+1==today[1] and first_day_list[2]+2==today[2] and first_day_list[3]==today[3] and i[5]=="passive":
                if available_balance > i[4]:
                    threading.Thread(target=doge.send_money, args=(str(i[4]), i[0], "default",)).start()
                    new_date = str(today[0])+"/"+str(today[1])+"/"+str(today[2])+"/"+str(today[3])
                    sql1.update_date(i[1], new_date)
                    sql1.update_status(i[1], "active")
                    docker.con_restart(i[1])
                    #print("Passive turned active")
                    threading.Thread(target=sendmaill_msg, args=(email, "Your computer has turned from passive to active!",)).start()
                else:
                    threading.Thread(target=delete_docker, args=(i[1],)).start()
                    sql1.delete_user_pc(i[1])
                    threading.Thread(target=sendmaill_msg, args=(email, "Your computer has been deleted because you don't have enough money in your wallet.",)).start()
                    #print("Computer deleted because of no money in wallet.")
    except Exception as e:
        print(e)
    mycount+=1
    print(mycount)
    time.sleep(60)
