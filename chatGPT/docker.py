import subprocess
import random

def bash(command):
	cmdlist = command.split(" ")
	output = subprocess.run(cmdlist, capture_output=True)
	output = output.stdout.decode("utf-8")
	return output

def get_open_ports():
	outlist = bash("lsof -i -P -n").split("\n")
	newlist = []
	for i in outlist:
		if "(LISTEN)" in i:
			n1 = i.find(":")
			n2 = i.find(" (LISTEN)")
			i = i[n1+1:n2]
			newlist.append(int(i))
	return newlist

def get_names():
	docker_names = bash('docker ps --format "{{.Names}}"').replace('"', '').split('\n')
	docker_names.pop(-1)
	return docker_names

def get_sizes():
	docker_sizes = bash('docker ps --format "{{.Size}}"').replace('"', '').split('\n')
	a=0
	for i in docker_sizes:
		no = i.find(" (virtual")
		i = i[0:no]
		docker_sizes[a] = i
		a+=1
	return docker_sizes

def get_ports0(): #Get detailed Ports
	docker_ports = bash('docker ps --format "{{.Ports}}"').replace('"', '').split('\n')
	return docker_ports

def get_ports1(): #Get all published ports
	docker_ports = bash('docker ps --format "{{.Ports}}"').replace('"', '').split('\n')
	portlist = []
	for i in docker_ports:
		while 1:
			a1 = i.find("0.0.0.0:")
			a2 = i.find("-")
			if a1==-1 or a2==-1:
				break
			port = i[a1+8:a2]
			i = i[a2+1:-1]
			a2 = i.find("-")
			i = i[a2+1:-1]
			portlist.append(port)
	return portlist

def create_docker(name, image, hostports, conports):
	mystr0="docker run"
	mystr1=" --name {} -d -i -t --cpus=.2 --memory=256m {} /bin/sh"
	newstr=""
	for i in range(len(hostports)):
		newstr+=" -p {}:{}".format(hostports[i], conports[i])
	bash(mystr0+newstr+mystr1.format(name, image))
	return "Docker created Name:{}".format(name)

def delete_docker(name):
	bash("docker stop {}".format(name))
	bash("docker rm {}".format(name))
	return 1

def con_run(name, command):
	bash("docker exec -it {} {}".format(name, command))
	return 1

def con_restart(name):
	bash("docker restart "+name)
	con_run(name, "service ssh restart")
	return 1

def restart_all():
	for i in get_names():
		if i == "portainer":
			pass
		else:
			con_restart(i)
	return 1

def clone_img(con_name, new_image_name): # clone image from stopped container
	bash("docker commit {} {}".format(con_name, new_image_name))
	return 1

######## New Functions #########

def printall():
	docker_names = get_names()
	docker_sizes = get_sizes()
	docker_ports = get_ports1()

	for i in range(len(docker_names)):
	        print(docker_names[i], docker_sizes[i])
	for i in docker_ports:
	        print(i)

def create_root(name, password):
	while 1:
		a = random.randint(1024, 65535)
		if a not in get_open_ports():
			hostports = [a]
			conports = [22]
			break
	while len(hostports) < 10:
		a = random.randint(1024, 65535)
		if a not in get_open_ports():
			hostports.append(a)
			conports.append(a)

	create_docker(name, "stc:latest", hostports, conports)
	con_run(name, "expect /e1.expect {}".format(password))
	con_run(name, "rm /e1.expect /stc1.sh")
	con_run(name, "service ssh restart")
	return hostports

def get_size_from_name(name):
    name_list=get_names()
    size_list=get_sizes()
    for i in range(len(name_list)):
        #print(name_list[i], size_list[i])
        if name == name_list[i]:
            return size_list[i]
