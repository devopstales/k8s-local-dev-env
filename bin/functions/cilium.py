#!/usr/bin/env python3

import yaml

from .helepers import (
    which,
    run_command_stdout, 
    CONFIG_JSON, 
    APPHOME
)

from .docker import get_docker_network
from ipaddress import ip_network

CILIUM_CONFIG_PATH = APPHOME + "/apps/cni_cilium/cilium-values.yaml"
CILIUM_HELMFILE_PATH = APPHOME + "/apps/cni_cilium/cilium.yaml"
MONITORING_NS_PATH = APPHOME + "/apps/monitoring/ns.yaml"

#############################################################################
# Cilium Configs
#############################################################################

def gen_cilium_config():
    print("# Generating Cilium Config")
    cilium_base_config = {
        "kubeProxyReplacement": True,
        "k8sServiceHost": f"{CONFIG_JSON['network']['api_host']}",
        "k8sServicePort": f"{CONFIG_JSON['network']['api_port']}",
        "rollOutCiliumPods": True,
        "ipv4": {
            "enabled": True,
        },
        "ipv6": {
            "enabled": False,
        },
        "nodePort": {
            "enabled": True,
        },
        "hostPort": {
            "enabled": True,
        },
        "externalIPs": {
            "enabled": True,
        },
        "MTU": 1300,
        "pmtuDiscovery": {
            "enabled": True,
        },
        "ipam": {
            "mode": "kubernetes"
#            "mode": "cluster-pool",
#            "operator": {
#                "clusterPoolIPv4PodCIDRList": "10.43.0.0/16",
#                "clusterPoolIPv4MaskSize": 24,
#                "clusterPoolIPv6PodCIDRList": "fd00::/104",
#                "clusterPoolIPv6MaskSize": 120,
#            }
        },
        "loadBalancer": {
            "l7": {
                "backend": "envoy"
            }
        },
        "hubble": {
            "metrics": {
                "enabled": [
                    "dns",
                    "drop",
                    "tcp",
                    "flow:sourceContext=workload-name|reserved-identity;destinationContext=workload-name|reserved-identity",
                    "port-distribution",
                    "icmp",
                    "kafka:labelsContext=source_namespace,source_workload,destination_namespace,destination_workload,traffic_direction;sourceContext=workload-name|reserved-identity;destinationContext=workload-name|reserved-identity",
                    "policy:sourceContext=app|workload-name|pod|reserved-identity;destinationContext=app|workload-name|pod|dns|reserved-identity;labelsContext=source_namespace,destination_namespace",
                    "httpV2:exemplars=true;labelsContext=source_ip,source_namespace,source_workload,destination_ip,destination_namespace,destination_workload,traffic_direction",
                ],
            },
            "ui": {
                "enabled": True,
                "replicas": 1,
                "ingress": {
                    "enabled": True,
                    "hosts": ["cilium.kdev.intra"],
                    "tls": [
                        {
                            "secretName": "hubble-ingress-tls",
                            "hosts": ["cilium.kdev.intra"],
                        }
                    ]
                },
            },
            "frontend": {
                "server": {
                    "ipv6": {
                        "enabled": False,
                    }
                },
            },
            "relay": {
                "enabled": True,
            },
        },
        "operator": {
            "replias": 1
        }
    }

    if CONFIG_JSON['monitoring']["enabled"] == "true":
        cilium_base_config['hubble']['metrics'].update({"serviceMonitor": {"enabled": True}})
        cilium_base_config['hubble']['metrics'].update(
            {
                "dashboards": {
                    "enabled": True,
                    "namespace": "monitoring-system",
                    "annotations": {
                        "grafana_folder": "cilium"
                    }
                }
            }
        )
        cilium_base_config.update(
            {
                "dashboards": {
                    "enabled": True,
                    "namespace": "monitoring-system",
                    "annotations": {
                        "grafana_folder": "cilium"
                    }
                }
            }
        )
        cilium_base_config.update(
            {
                'prometheus': {
                    'enabled': True,
                    'serviceMonitor': {
                        'enabled': True,
                    }
                }
            }
        )
        cilium_base_config.update(
            {
                'envoy': {
                    'prometheus': {
                        'enabled': True,
                        'serviceMonitor': {
                            'enabled': True,
                        }
                    }
                }
            }
        )
        cilium_base_config.update(
            {
                'operator': {
                    'prometheus': {
                        'enabled': True,
                        'serviceMonitor': {
                            'enabled': True,
                        }
                    },
                    "dashboards": {
                        "enabled": True,
                        "namespace": "monitoring-system",
                        "annotations": {
                            "grafana_folder": "cilium"
                        }
                    }
                }
            }
        )

    if CONFIG_JSON['ingress']['driver'] == "nginx":
        cilium_base_config['hubble']['ui']['ingress'].update(
            {
                'annotations': {
                    "cert-manager.io/cluster-issuer": "ca-issuer",
                }
            }
        )
    elif CONFIG_JSON['ingress']['driver'] == "pomerium":
        cilium_base_config['hubble']['ui']['ingress'].update(
            {
                'annotations': {
                    "cert-manager.io/cluster-issuer": "ca-issuer",
                    "ingress.pomerium.io/allow_any_authenticated_user": True,
                }
            }
        )
    else:
        cilium_base_config['hubble']['ui']['ingress'].update(
            {
                'annotations': {
                    "cert-manager.io/cluster-issuer": "ca-issuer",
                }
            }
        )

    if CONFIG_JSON['network']['loadbalancer'] == "cilium":
        if CONFIG_JSON['network']['loadbalancer_mode'] == "l2":
            cilium_base_config.update(
                {
                    "l2announcements": {
                        "enabled": True
                    },
                    "externalIPs": {
                        "enabled": True
                    },
                }
            )
        if CONFIG_JSON['network']['loadbalancer_mode'] == "bgp":
            cilium_base_config.update(
                {
                    "bgpControlPlane": {
                        "enabled": True
                    },
                }
            )

    if CONFIG_JSON['network']['mtls'] == 'true':
        cilium_base_config.update(
            {
                "authentication": {
                    "mode": "required",
                    "mutual": {
                        "spire": {
                            "enabled": False,
                            "install": {
                                "enabled": False
                            }
                        }
                    }
                }
            }
        )

    if CONFIG_JSON['ingress']['driver'] == "cilium":
        cilium_base_config.update(
            {
                'ingressController': {
                    'default': True,
                    'enabled': True,
                    'loadbalancerMode': "shared"
                }
            }
        )

    if CONFIG_JSON['ingress']['apigateway'] == "cilium":
        cilium_base_config.update({
            'gatewayAPI': {
                'enabled': True,
            }
        }
    )

    with open(CILIUM_CONFIG_PATH, 'w') as yaml_file:
        yaml.dump(cilium_base_config, yaml_file, default_flow_style=False)

def install_cilium():
    KUBECTL_PATH = which("kubectl")
    RUN_KUBECTL = KUBECTL_PATH + " apply -f " + MONITORING_NS_PATH
    run_command_stdout(RUN_KUBECTL)

    HELMFILE_PATH = which("helmfile")
    RUN_COMMAND = HELMFILE_PATH + " apply -f " + CILIUM_HELMFILE_PATH
    print("# Install Cilium")
    run_command_stdout(RUN_COMMAND)

def install_loadbalancer():
    print("# Install LoadBalancer")
    if CONFIG_JSON['network']['loadbalancer_mode'] == "l2":
        network_data = get_docker_network("kind")
        docker_network_subnet = network_data["IPAM"]['Config'][0]['Subnet']
        network_subnets = list(ip_network(docker_network_subnet).subnets(new_prefix=24))
        lb_network_subnet = str(network_subnets[-1])

        LBPOOL_FILE_PATH =  APPHOME + "/apps/lb_cilium_l2/cilium-pool.yaml"
        ANNOUNCEMET_FILE_PATH =  APPHOME + "/apps/lb_cilium_l2/l2-announcement.yaml"

        cilium_pool = {
            "apiVersion": "cilium.io/v2alpha1",
            "kind": "CiliumLoadBalancerIPPool",
            "metadata":{
                "name": "kind-pool",
            },
            "spec": {
                "blocks":[
                    {
                        "cidr": f"{lb_network_subnet}"
                    }
                ]
            }
        }

        with open(LBPOOL_FILE_PATH, 'w') as yaml_file:
            yaml.dump(cilium_pool, yaml_file, default_flow_style=False)

        KUBECTL_PATH = which("kubectl")
        RUN_KUBECTL = KUBECTL_PATH + " apply -f " + LBPOOL_FILE_PATH
        run_command_stdout(RUN_KUBECTL)
        RUN_KUBECTL = KUBECTL_PATH + " apply -f " + ANNOUNCEMET_FILE_PATH
        run_command_stdout(RUN_KUBECTL)
