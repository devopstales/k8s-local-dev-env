#!/usr/bin/env python3

import yaml

from .helepers import (
    which,
    run_command_stdout,
    APPHOME,
    CONFIG_JSON,
)

KIND_INIT_CONFIG_PATH = APPHOME + "/mounts/cilium-entrypoint.sh" + ":/bin/cilium-entrypoint.sh"
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

    print("# Generate KIND Config")
    with open(KIND_CONFIG_PATH, 'w') as yaml_file:
        yaml.dump(kind_base_config, yaml_file, default_flow_style=False)

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
