import subprocess

def bash(command):
	cmdlist = command.split(" ")
	output = subprocess.run(cmdlist, capture_output=True)
	output = output.stdout.decode("utf-8")
	return output

def get_names():
	docker_names = bash('docker ps --format "{{.Names}}"').replace('"', '').split('\n')
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
	mystr1=" --name {} -d -i -t {} /bin/sh"
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

def clone_img(con_name, new_image_name):
	bash("docker commit {} {}".format(con_name, new_image_name))
	return 1
