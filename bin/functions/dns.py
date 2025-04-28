#!/usr/bin/env python3


from .helepers import (
    which,
    run_command_stdout
)

from .docker import get_docker_network
from ipaddress import ip_network


#############################################################################
# Variables
#############################################################################

from .helepers import APPHOME, CONFIG_JSON
from .ingress import INGRESS_TYPE

DNS_CONFIG_FILE = APPHOME + "config/coredns/coredns-config.yaml"

if CONFIG_JSON['network']['driver'] == "cilium-helm":
    if CONFIG_JSON['network']['loadbalancer'] == "cilium":
        if CONFIG_JSON['monitoring']['enabled'] == "true":
            DNS_TYPE="environment=loadbalancer-monitoring"
        else:
            DNS_TYPE="environment=loadbalancer"
        DNS_DEPLOY_TYPE = "external-dns"
else:
    if INGRESS_TYPE == "nginx":
        DNS_DEPLOY_TYPE = "minikub-dns"
    else:
        DNS_DEPLOY_TYPE = None
        
#############################################################################
# Functions
#############################################################################

def generate_dns_config():
    network_data = get_docker_network("kdev")
    docker_network_subnet = network_data["IPAM"]['Config'][0]['Subnet']
    network_subnets = list(ip_network(docker_network_subnet).subnets(new_prefix=24))
    network_hosts = list(network_subnets[-1].hosts())
    DNS_SERVER_IP = str(network_hosts[0])
    coredns_config = f"""apiVersion: v1
data:
  Corefile: |
    .:53 {{
        errors
        health {{
           lameduck 5s
        }}
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {{
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }}
        prometheus :9153
        forward . /etc/resolv.conf {{
           max_concurrent 1000
        }}
        cache 30
        loop
        reload
        loadbalance
    }}
    kdev.intra:53 {{
        errors
        cache 30
        forward . {DNS_SERVER_IP}
    }}
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
"""
    print(coredns_config)

def create_dns_server():
    HELMFILE_PATH = which("helmfile")
    KUBECTL_PATH = which("kubectl")
    MINIKUBE_PATH = which("minikube")

    if DNS_DEPLOY_TYPE == "external-dns":
        print("# Install DNS server")

        RUN_KUBECTL = KUBECTL_PATH + " apply -f " + APPHOME + "/apps/cluster_system/ns.yaml"
        run_command_stdout(RUN_KUBECTL)

        RUN_COMMAND = HELMFILE_PATH + "  apply -q -f  " + APPHOME + "/apps/cluster_system/etcd.yaml"
        print("## Install ETCD server")
        run_command_stdout(RUN_COMMAND)

        RUN_COMMAND = HELMFILE_PATH + "  apply -q -f  " + APPHOME + "/apps/cluster_system/coredns.yaml -l " + DNS_TYPE
        print("## Install CoreDNS server")
        run_command_stdout(RUN_COMMAND)

        RUN_COMMAND = HELMFILE_PATH + "  apply -q -f  " + APPHOME + "/apps/cluster_system/external-dns.yaml"
        print("## Install External DNS")
        run_command_stdout(RUN_COMMAND)
    elif DNS_DEPLOY_TYPE == "minikub-dns":
        MINIKUBE_COMMAND = MINIKUBE_PATH + " -p kdev addons enable ingress-dns"
        print("# Install DNS server")
        run_command_stdout(MINIKUBE_COMMAND)
