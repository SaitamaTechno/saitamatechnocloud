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
#print(docker.create_docker("saitama1", "stc1", [1000], [22]))
#print(docker.con_run("saitama1", "bash /expect1.sh 123456aaa"))
#print(docker.con_run("saitama1", "rm /expect1.sh /stc1.sh"))
docker.delete_docker("saitama1")
printall()
