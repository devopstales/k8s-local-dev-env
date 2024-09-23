#!/usr/bin/env python3

from ipaddress import ip_network

from .helepers import CONFIG_JSON, ROOT_CERT_PATH
from .docker import get_docker_network

import docker
from netaddr import IPNetwork

#############################################################################
## Print Mesage
#############################################################################

def print_messages(type):
    print("#############################################################################\n#")
    #if type == "base":
    #    print("# Certificate Generated: Add %s to trusted Certificates\n#" % ROOT_CERT_PATH)

    if type == "base":
        print("# Certificate Generated: Add %s to trusted Certificates\n#" % ROOT_CERT_PATH)

        if CONFIG_JSON['network']['loadbalancer'] == "cilium" and \
            CONFIG_JSON['network']['loadbalancer_mode'] == "l2":
                network_data = get_docker_network("kind")
                docker_network_subnet = network_data["IPAM"]['Config'][0]['Subnet']
                network_subnets = list(ip_network(docker_network_subnet).subnets(new_prefix=24))
                network_hosts = list(network_subnets[-1].hosts())
                DNS_SERVER_IP = str(network_hosts[0])
                print("# DNS server is tunning: Set your DNS server to %s\n#" % DNS_SERVER_IP)

        if CONFIG_JSON['registry']['enabled'] == "true":
            print("# Add registry as insecure:")
            
            d = docker.from_env()
            container = d.containers.get("docker_registry")
            network = d.networks.get("kind")
            registry_ip_network = network.attrs['Containers'][container.id]['IPv4Address']
            REGISTRY_IP = IPNetwork(registry_ip_network).ip

            print('#\t/etc/docker/daemon.json: ')
            print('#\t\t { "insecure-registries": [ "%s:5000" ] }\n#' % REGISTRY_IP)

    print("#############################################################################")