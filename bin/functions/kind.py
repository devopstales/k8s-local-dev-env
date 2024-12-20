#!/usr/bin/env python3

import yaml

from .helepers import (
    which,
    run_command_stdout,
    APPHOME,
    CONFIG_JSON,
)

from .docker import get_docker_registry_ip

import docker
from netaddr import IPNetwork

KIND_CONFIG_PATH = APPHOME + "/config/kind-config.yaml"

#############################################################################
# kind Configs
#############################################################################

def gen_kind_config():
    kind_base_config = {
        "kind": "Cluster",
        "apiVersion": "kind.x-k8s.io/v1alpha4",
        "nodes": [
            {
                "role": "control-plane"
            }
        ],
        "networking": {
            "disableDefaultCNI": True,
            "kubeProxyMode": "none",
            "ipFamily": "ipv4",
            "apiServerAddress": "127.0.0.1",
            "podSubnet":   f"{CONFIG_JSON['network']['cluster_cidr']}",
            "serviceSubnet": f"{CONFIG_JSON['network']['service_cidr']}",
        }
    }

    if CONFIG_JSON["network"]["loadbalancer"] != "cilium":
        kind_base_config["nodes"][0].update(
            {
                "extraPortMappings": [
                    {
                        "containerPort": 80,
                        "hostPort": 80,
                        "listenAddress": "127.0.0.1",
                        "protocol": "TCP"
                    },
                    {
                        "containerPort": 443,
                        "hostPort": 443,
                        "listenAddress": "127.0.0.1",
                        "protocol": "TCP"
                    },
                ]
            },
        )

    if CONFIG_JSON['registry']['enabled'] == "true":
        REGISTRY_IP = get_docker_registry_ip()
        kind_registry_config = f"""containerdConfigPatches:
- |-
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."registry.kdev.intra:5000"]
    endpoint = ["http://registry.kdev.intra:5000"]
  [plugins."io.containerd.grpc.v1.cri".registry.configs."registry.kdev.intra:5000".tls]
    insecure_skip_verify = true
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors."{REGISTRY_IP}:5000"]
    endpoint = ["http://{REGISTRY_IP}:5000"]
  [plugins."io.containerd.grpc.v1.cri".registry.configs."{REGISTRY_IP}:5000".tls]
    insecure_skip_verify = true
"""
        
    if CONFIG_JSON['sso']['enabled'] == 'true':
        kind_sso_config = f"""kubeadmConfigPatches:
- |-
  kind: ClusterConfiguration
  apiServer:
    extraArgs:
      oidc-client-id: kind
      oidc-issuer-url: https://keycloak.kdev.intra/auth/realms/kind-apps
      oidc-username-claim: email
      oidc-groups-claim: groups
"""
#   oidc-ca-file: /etc/ca-certificates/keycloak/root-ca.pem


    print("# Generate KIND Config")
    with open(KIND_CONFIG_PATH, 'w') as yaml_file:
        yaml.dump(kind_base_config, yaml_file, default_flow_style=False)
        if CONFIG_JSON['registry']['enabled'] == "true":
            yaml_file.write(kind_registry_config)
        if CONFIG_JSON['sso']['enabled'] == 'true':
            yaml_file.write(kind_sso_config)

def delete_kind_config():
    NotImplemented

#############################################################################
# kind
#############################################################################


def start_kind():
    KIND_PATH = which("kind")
    RUN_COMMAND = KIND_PATH + " create cluster --config=" + KIND_CONFIG_PATH
    print("# Start kind cluster")
    run_command_stdout(RUN_COMMAND)


def delete_kind():
    KIND_PATH = which("kind")
    RUN_COMMAND = KIND_PATH + "  delete clusters kind"
    print("# Delete kind cluster")
    run_command_stdout(RUN_COMMAND)

def load_docker_image(image_name):
    KIND_PATH = which("kind")
    RUN_COMMAND = KIND_PATH + " load docker-image " + image_name
    run_command_stdout(RUN_COMMAND)
