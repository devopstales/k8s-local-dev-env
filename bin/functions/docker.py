#!/usr/bin/env python3

import docker
from .helepers import CONFIG_JSON, APPHOME

import yaml, json, sys
import ruamel.yaml

from netaddr import IPNetwork

KIND_CONFIG_PATH = APPHOME + "/config/local-registry-config.yaml"

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

#    container = d.containers.get("docker_registry")
#    network = d.networks.get("kind")
#    registry_ip_network = network.attrs['Containers'][container.id]['IPv4Address']
#    REGISTRY_IP = IPNetwork(registry_ip_network).ip
#    kind_registry_config = f"""apiVersion: v1
#kind: ConfigMap
#metadata:
#  name: local-registry-hosting
#  namespace: kube-public
#data:
#  local_registry_hosting: |
#    help: "https://github.com/kubernetes/enhancements/tree/master/keps/sig-cluster-lifecycle/generic/1755-communicating-a-local-registry#specification-for-localregistryhosting-v1"
#    host: "{REGISTRY_IP}:5000"
#    HostFromContainerRuntime: "{REGISTRY_IP}:5000"
#"""
#
#    with open(KIND_CONFIG_PATH, 'w') as yaml_file:
#        yaml_file.write(kind_registry_config)

def stop_registry():
    d = docker.from_env()
    try:
        container = d.containers.get("docker_registry")
        container.remove(force=True)
    except:
        pass
