import sql1
import docker
import threading
import datetime
from sys import exit

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
    year, month, day=date.year, date.month, date.day
    return [year, month, day]

for i in sql1.get_data_pc():
    print(i)
    today=get_date()
    name=i[1]
    size=docker.get_size_from_name(name)
    if size[-2]=="G":
        size=float(size.replace("GB", ""))
        print(size)
        if size>i[3]:
            print("deleted", name)
            threading.Thread(target=delete_docker, args=(name,)).start()
            sql1.delete_user_pc(name)
    first_day=i[6]
    first_day_list=[int(i) for i in first_day.split("/")]
    print(first_day_list)
    if first_day[0]==today[0] and today[1]==first_day[1]+1 and first_day[2]==today[2] and i[5]=="active":
        #Code for payment
        print("I got a payment.")
