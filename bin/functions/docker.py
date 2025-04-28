#!/usr/bin/env python3

import docker
from netaddr import IPNetwork
from ipaddress import ip_network

#############################################################################
## Variables
#############################################################################

from .helepers import CONFIG_JSON

#############################################################################
## Docker functions
#############################################################################

def create_docker_network():
    is_network = False
    d = docker.from_env()
    for n in d.networks.list():
        if n.name == "kdev":
            is_network = True

    if not is_network:
        ipam_pool = docker.types.IPAMPool(
            subnet  = CONFIG_JSON['network']['subnet'],
            gateway = CONFIG_JSON['network']['gateway']
        )

        ipam_config = docker.types.IPAMConfig(
            pool_configs=[ipam_pool]
        )

        print("# Create Docker Network")
        d.networks.create(
            "kdev",
            driver="bridge",
            ipam=ipam_config,
            labels={
                "created_by.minikube.sigs.k8s.io": "true",
                "name.minikube.sigs.k8s.io": "kdev",
                "app": "kdev"
            },
            options={
                "--icc": "",
                "--ip-masq": "",
                "com.docker.network.driver.mtu": "1500"
            }
        )

def delete_docker_network():
    d = docker.from_env()
    for n in d.networks.list():
        if n.name == "kdev":
            print("# Delete Docker Network")
            n.remove()


def get_docker_network():
    d = docker.from_env()
    network = d.networks.get("kdev")
    return network.attrs

def get_container(name):
    d = docker.from_env()
    container = d.containers.get(name)
    return container

#############################################################################
# Get IPs
#############################################################################

def get_hots_ip():
    """
    Get teh IP address off the host in the docker network. \n
    It is the first ip address off the docker network.
    """
    network_data = get_docker_network()
    docker_network_subnet = network_data["IPAM"]['Config'][0]['Subnet']
    network_hosts = list(IPNetwork(docker_network_subnet).iter_hosts())
    HOST_IP = str(network_hosts[0])
    return HOST_IP

def get_master_ip():
    """
    Get the ip address of the kind master from docker network.
    """
    container = get_container("kdev")
    network_data = get_docker_network()
    master_ip_network = network_data['Containers'][container.id]['IPv4Address']
    MASTER_IP = IPNetwork(master_ip_network).ip
    return MASTER_IP

def get_loadbalancer_subnet():
    """
    If loadbalancer mode is `l2` get last /24 subnet for Loadbalancer subnet. \n
    If loadbalancer mode is `bgp` get value from `config.ini`
    """
    if CONFIG_JSON['network']['loadbalancer_mode'] == "l2":
        network_data = get_docker_network()
        docker_network_subnet = network_data["IPAM"]['Config'][0]['Subnet']
        network_subnets = list(ip_network(docker_network_subnet).subnets(new_prefix=24))
        LOADBALANCER_SUBENT = str(network_subnets[-1])
        return LOADBALANCER_SUBENT
    else:
        LOADBALANCER_SUBENT = CONFIG_JSON['network']['loadbalancer_cidr']
        return LOADBALANCER_SUBENT

def get_dns_server_ip():
    """
    Get DNS Server IP
    """
    network_data = get_docker_network()
    docker_network_subnet = network_data["IPAM"]['Config'][0]['Subnet']
    network_subnets = list(ip_network(docker_network_subnet).subnets(new_prefix=24))
    network_hosts = list(network_subnets[-1].hosts())
    DNS_SERVER_IP = str(network_hosts[0])
    return DNS_SERVER_IP