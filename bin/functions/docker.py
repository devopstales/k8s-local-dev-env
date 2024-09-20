#!/usr/bin/env python3

import docker
from .helepers import CONFIG_JSON

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
    d = docker.from_env()
    d.containers.run(
        name="docker_registry",
        detach=True,
        restart_policy="always",
        ports={'5000/tcp': ('127.0.0.1', 5000)},
        network="kind",
        network_mode="bridge",
        image="registry:2",
        volumes=[
            "/var/lib/docker-registry:/var/lib/docker-registry"
        ]
    )

def stop_registry():
    d = docker.from_env()
    container = d.get("docker_registry")
    container.remove(
        forece= True,
    )


