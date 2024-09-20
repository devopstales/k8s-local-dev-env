#!/usr/bin/env python3

from ipaddress import ip_network

from .helepers import CONFIG_JSON, ROOT_CERT_PATH
from .docker import get_docker_network



#############################################################################
## Print Mesage
#############################################################################

def print_messages(type):
    print("#############################################################################")
    if type == "base":
        print("# Certificate Geberated: Add %s to trusted Certificates" % ROOT_CERT_PATH)

    if type == "all":
        print("# Certificate Geberated: Add %s to trusted Certificates" % ROOT_CERT_PATH)
        if CONFIG_JSON['network']['loadbalancer'] == "cilium" and \
            CONFIG_JSON['network']['loadbalancer_mode'] == "l2":
                network_data = get_docker_network("kind")
                docker_network_subnet = network_data["IPAM"]['Config'][0]['Subnet']
                network_subnets = list(ip_network(docker_network_subnet).subnets(new_prefix=24))
                network_hosts = list(network_subnets[-1].hosts())
                DNS_SERVER_IP = str(network_hosts[0])
                print("# DNS server is tunning: Set your DNS server to %s" % DNS_SERVER_IP)