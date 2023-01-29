import docker

#docker.bash("ls -al")
def printall():
	docker_names = docker.get_names()
	docker_sizes = docker.get_sizes()
	#docker_ports0 = docker.get_ports0()
	docker_ports = docker.get_ports1()

	for i in range(len(docker_names)):
		print(docker_names[i], docker_sizes[i])
	for i in docker_ports:
		print(i)
printall()
print(docker.create_docker("saitama1", "stc:latest", [1001, 1002], [22, 1002]))
print(docker.con_run("saitama1", "expect /e1.expect 123456aaa"))
print(docker.con_run("saitama1", "rm /e1.expect /stc1.sh"))
print(docker.con_run("saitama1", "service ssh restart"))
#docker.delete_docker("saitama1")
#docker.clone_img("python3", "stc")
printall()
