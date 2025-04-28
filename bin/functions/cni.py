#!/usr/bin/env python3

import yaml

from .helepers import (
    which,
    run_command_stdout
)

from .docker import get_hots_ip, get_master_ip

from .docker import get_docker_network, get_loadbalancer_subnet,\
    get_hots_ip, get_master_ip

from ipaddress import ip_network

#############################################################################
# Variables
#############################################################################

from .helepers import CONFIG_JSON, APPHOME

MONITORING_NS_PATH = APPHOME + "/apps/monitoring/ns.yaml"

CILIUM_HELMFILE_PATH = APPHOME + "/apps/cni_cilium/cilium.yaml"
CILIUM_IP_PUUL_CONFIG_PATH = APPHOME + "/apps/lb_cilium/cilium-pool.yaml"
CILIUM_CONFIG_PATH = APPHOME + "/apps/cni_cilium/cilium-values.yaml"


FRR_CONFIG_PATH = APPHOME + "/config/frr/frr.conf"
LBPOOL_FILE_PATH =  APPHOME + "/config/cilium/cilium-pool.yaml"
CILIUM_BGP_POLICY_PATH = APPHOME + "/config/cilium/bgp-policy.yaml"

#############################################################################
# Functions
#############################################################################

def start_cni_network(CNI_DRIVER):
    if CNI_DRIVER == "false": # => cilium-helm or cilium cni with LB
        gen_cilium_config()
        install_cilium()
        install_loadbalancer()
    
#############################################################################
# Cilium Configs
#############################################################################

def gen_cilium_config():
    print("# Generating Cilium Config")
    MASTER_IP = get_master_ip()

    cilium_base_config = {
        "kubeProxyReplacement": True,
        "k8sServiceHost": f"{MASTER_IP}",
        "k8sServicePort": "8443",
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
                    "className": "default",
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
            "replicas": 1
        }
    }

    if CONFIG_JSON['service_mesh']["driver"] == "cilium":
        #   "mode": "required",
        cilium_base_config.update(
            {
                "authentication": {
                    "mutual": {
                        "spire": {
                             "enabled": True,
                             "install": {
                                 "enabled": True,
                             }
                        }
                    }
                }
            }
        )

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
                    "ingress.pomerium.io/allow_any_authenticated_user": "true",
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
            # BGP Pearing Policy Configuration
            host_IP = get_hots_ip()
            cilium_bgp_pearing_policy_config = {
                "apiVersion": "cilium.io/v2alpha1",
                "kind": "CiliumBGPPeeringPolicy",
                "metadata": {
                    "name": "bgp-peering-policy"
                },
                "spec": {
                    "virtualRouters": [
                        {
                            "localASN": 64512,
                            "exportPodCIDR": False,
                            "neighbors": [
                                {
                                    "peerAddress": host_IP+"/32",
                                    "peerASN": 64513
                                }
                            ],
                            "serviceSelector": {
                                "matchExpressions": [
                                    {
                                        "key": "somekey",
                                        "operator": "NotIn",
                                        "values": ['never-used-value']
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
            with open(CILIUM_BGP_POLICY_PATH, 'w') as yaml_file:
                yaml.dump(cilium_bgp_pearing_policy_config, yaml_file, default_flow_style=False)
        # Generate IP Pool
        loadbalancer_cidr = str(get_loadbalancer_subnet())
        cilium_ip_pool_config = {
            "apiVersion": "cilium.io/v2alpha1",
            "kind": "CiliumLoadBalancerIPPool",
            "metadata": {
                "name": "base-pool"
            },
            "spec": {
                "allowFirstLastIPs": "No",
                "blocks": [
                    {
                        "cidr": loadbalancer_cidr
                    }
                ]
            }
        }
        with open(CILIUM_IP_PUUL_CONFIG_PATH, 'w') as yaml_file:
            yaml.dump(cilium_ip_pool_config, yaml_file, default_flow_style=False)

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

    if CONFIG_JSON['service_mesh']['apigateway'] == "cilium":
        cilium_base_config.update({
            'gatewayAPI': {
                'enabled': True,
            }
        }
    )

    with open(CILIUM_CONFIG_PATH, 'w') as yaml_file:
        yaml.dump(cilium_base_config, yaml_file, default_flow_style=False)

#############################################################################
# Cilium LB
#############################################################################

def install_loadbalancer():
    if CONFIG_JSON['network']['loadbalancer'] == "cilium":
        print("# Install LoadBalancer")
        if CONFIG_JSON['network']['loadbalancer_mode'] == "l2":
            network_data = get_docker_network()
            docker_network_subnet = network_data["IPAM"]['Config'][0]['Subnet']
            network_subnets = list(ip_network(docker_network_subnet).subnets(new_prefix=24))
            lb_network_subnet = str(network_subnets[-1])

            ANNOUNCEMET_FILE_PATH =  APPHOME + "/apps/lb_cilium/l2-announcement.yaml"
            TEST_FILE_PATH = APPHOME + "/apps/lb_cilium/lb-test.yaml"

            cilium_pool = {
                "apiVersion": "cilium.io/v2alpha1",
                "kind": "CiliumLoadBalancerIPPool",
                "metadata":{
                    "name": "base-pool",
                },
                "spec": {
                    "blocks":[
                        {
                            "cidr": lb_network_subnet
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
            RUN_KUBECTL = KUBECTL_PATH + " apply -f " + TEST_FILE_PATH
            run_command_stdout(RUN_KUBECTL)
            
        if CONFIG_JSON['network']['loadbalancer_mode'] == "bgp":
            generate_frr_config()
            KUBECTL_PATH = which("kubectl")
            RUN_KUBECTL = KUBECTL_PATH + " apply -f " + CILIUM_IP_PUUL_CONFIG_PATH
            run_command_stdout(RUN_KUBECTL)
            RUN_KUBECTL = KUBECTL_PATH + " apply -f " + CILIUM_BGP_POLICY_PATH
            run_command_stdout(RUN_KUBECTL)


#############################################################################
# Cilium CNI
#############################################################################

def install_cilium():
    KUBECTL_PATH = which("kubectl")
    RUN_KUBECTL = KUBECTL_PATH + " apply -f " + MONITORING_NS_PATH
    run_command_stdout(RUN_KUBECTL)

    HELMFILE_PATH = which("helmfile")
    RUN_COMMAND = HELMFILE_PATH + " apply -q -f " + CILIUM_HELMFILE_PATH
    print("# Install Cilium")
    run_command_stdout(RUN_COMMAND)
    
#############################################################################
# FRR Router
#############################################################################

def generate_frr_config():
    HOST_IP = get_hots_ip()
    MATER_IP = get_master_ip()
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