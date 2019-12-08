import socket
import os
import subprocess

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1", 80))
    private_ip = s.getsockname()[0]
    s.close()

    return private_ip

def main():
    # get the private ip of the VM
    private_ip = get_private_ip()

    CASSANDRA_BROADCAST_ADDRESS = private_ip
    CASSANDRA_ENDPOINT_SNITCH = "GossipingPropertyFileSnitch"
    CASSANDRA_DC = "tx"
    CASSANDRA_RACK = "rack1"
    CASSANDRA_CLUSTER_NAME = "cassandracluster"
    CASSANDRA_SEEDS= "192.168.105.1"
    CASSANDRA_VERSION = "3.11.5"

    #build the docker run command
    #  docker run --name cassandra -d -e CASSANDRA_BROADCAST_ADDRESS=192.168.105.2 -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch -e CASSANDRA_DC=tx -e CASSANDRA_RACK=rack1 -e CASSANDRA_CLUSTER_NAME=testcluster -e CASSANDRA_SEEDS=192.168.105.1 -p 7000:7000 -p 9042:9042 -v ~/cassandra_data:/var/lib/cassandra cassandra:3.11.5
    docker_command = "docker run --name cassandra -d -e CASSANDRA_BROADCAST_ADDRESS={} -e CASSANDRA_ENDPOINT_SNITCH={} -e CASSANDRA_DC={} -e CASSANDRA_RACK={} -e CASSANDRA_CLUSTER_NAME={} -e CASSANDRA_SEEDS={} -p 7000:7000 -p 9042:9042 -v cassandra_data:/var/lib/cassandra cassandra:{}".format(CASSANDRA_BROADCAST_ADDRESS, CASSANDRA_ENDPOINT_SNITCH, CASSANDRA_DC, CASSANDRA_RACK, CASSANDRA_CLUSTER_NAME, CASSANDRA_SEEDS, CASSANDRA_VERSION)

    directory = "cassandra_data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    subprocess.run(docker_command.split(" "))

    # print(docker_command)

main()
