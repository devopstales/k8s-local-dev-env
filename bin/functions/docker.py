#!/usr/bin/env python3

import docker, yaml
from .helepers import CONFIG_JSON, APPHOME

from netaddr import IPNetwork
from ipaddress import ip_network

KIND_CONFIG_PATH = APPHOME + "/config/local-registry-config.yaml"
FRR_MOUNT_PATH = APPHOME + "/mounts/frr/"
FRR_CONFIG_PATH = FRR_MOUNT_PATH + "frr.conf"

#############################################################################
## Docker functions
#############################################################################

def create_docker_network():
    is_network = False
    d = docker.from_env()
    for n in d.networks.list():
        if n.name == "kind":
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
            "kind",
            driver="bridge",
            ipam=ipam_config,
            labels={
                 "app": "kdev",
            },
            options={
                "com.docker.network.bridge.enable_ip_masquerade": "true",
                "com.docker.network.driver.mtu": "1500"
            }
        )

def delete_docker_network():
    d = docker.from_env()
    for n in d.networks.list():
        if n.name == "kind":
            print("# Delete Docker Network")
            n.remove()


def get_docker_network(name):
    d = docker.from_env()
    network = d.networks.get(name)
    return network.attrs

def get_container_network(name):
    d = docker.from_env()
    container = d.containers.get(name)
    return container

#############################################################################
# Registry
#############################################################################

def start_registry():
    REGISTRY_PORT = CONFIG_JSON['registry']['port']
    REGISTRY_FOLDER = CONFIG_JSON['registry']['rootdirectory']
    d = docker.from_env()
    d.containers.run(
        name="docker_registry",
        detach=True,
        restart_policy={"Name": "always"},
        ports={'5000/tcp': ('127.0.0.1', REGISTRY_PORT)},
        network="kind",
        image="registry:2",
        volumes=[
            f"{REGISTRY_FOLDER}:/var/lib/registry",
        ]
    )

def stop_registry():
    d = docker.from_env()
    try:
        container = get_container_network("docker_registry")
        container.remove(force=True)
    except:
        pass

#############################################################################
# FRR Router
#############################################################################

def generate_frr_config():
    HOST_IP = get_hots_ip()
    MATER_IP = get_kind_master_ip()
    frr_config =  f"""!
log syslog notifications
frr defaults traditional
!
router bgp 64513
no bgp ebgp-requires-policy
bgp router-id {HOST_IP}
!
neighbor {MATER_IP} remote-as 64512
neighbor {MATER_IP} update-source {MATER_IP}
neighbor {MATER_IP} soft-reconfiguration inbound
!
address-family ipv4 unicast
neighbor {MATER_IP} next-hop-self
exit-address-family
!
address-family ipv6 unicast
exit-address-family
!
line vty
"""
    with open(FRR_CONFIG_PATH, 'w') as file:
        file.write(frr_config)

#############################################################################
# Get IPs
#############################################################################

def get_dns_server_ip():
    """
    Get DNS Server IP
    """
    network_data = get_docker_network("kind")
    docker_network_subnet = network_data["IPAM"]['Config'][0]['Subnet']
    network_subnets = list(ip_network(docker_network_subnet).subnets(new_prefix=24))
    network_hosts = list(network_subnets[-1].hosts())
    DNS_SERVER_IP = str(network_hosts[0])
    return DNS_SERVER_IP

def get_docker_registry_ip():
    """
    Get Docker Registry IP
    """
    d = docker.from_env()
    container = get_container_network("docker_registry")
    network = get_docker_network("kind")
    registry_ip_network = network['Containers'][container.id]['IPv4Address']
    REGISTRY_IP = IPNetwork(registry_ip_network).ip
    return REGISTRY_IP

def get_loadbalancer_subnet():
    """
    If loadbalancer mode is `l2` get last /24 subnet for Loadbalancer subnet. \n
    If loadbalancer mode is `bgp` get value from `config.ini`
    """
    if CONFIG_JSON['network']['loadbalancer_mode'] == "l2":
        network_data = get_docker_network("kind")
        docker_network_subnet = network_data["IPAM"]['Config'][0]['Subnet']
        network_subnets = list(ip_network(docker_network_subnet).subnets(new_prefix=24))
        LOADBALANCER_SUBENT = str(network_subnets[-1])
        return LOADBALANCER_SUBENT
    else:
        LOADBALANCER_SUBENT = CONFIG_JSON['network']['loadbalancer_cidr']
        return LOADBALANCER_SUBENT

def get_hots_ip():
    """
    Get teh IP address off the host in the docker network. \n
    It is the first ip address off the docker network.
    """
    network_data = get_docker_network("kind")
    docker_network_subnet = network_data["IPAM"]['Config'][0]['Subnet']
    network_hosts = list(IPNetwork(docker_network_subnet).iter_hosts())
    HOST_IP = str(network_hosts[0])
    return HOST_IP

def get_kind_master_ip():
    """
    Get the ip address of the kind master from docker network.
    """
    container = get_container_network("kind-control-plane")
    network_data = get_docker_network("kind")
    master_ip_network = network_data['Containers'][container.id]['IPv4Address']
    MASTER_IP = IPNetwork(master_ip_network).ip
    return MASTER_IP