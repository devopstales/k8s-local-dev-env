#!/usr/bin/env python3

from .helepers import CONFIG_JSON, ROOT_CERT_PATH
from .docker import get_dns_server_ip, get_docker_registry_ip

#############################################################################
## Print Mesage
#############################################################################

def print_messages(type):
    print("#############################################################################\n#")
    if type == "base":
        print("# Certificate Generated: Add %s to trusted Certificates\n#" % ROOT_CERT_PATH)

    if type == "all":
        print("# Certificate Generated: Add %s to trusted Certificates\n#" % ROOT_CERT_PATH)

        if CONFIG_JSON['network']['loadbalancer'] == "cilium":
            DNS_SERVER_IP = get_dns_server_ip()
            print("# DNS server is running: Set your DNS server to %s\n#" % DNS_SERVER_IP)
            print("# Loadbalancer is running in %s mode" % CONFIG_JSON['network']['loadbalancer_mode'])
            if CONFIG_JSON['network']['loadbalancer_mode'] == "bgp":
                print("# test with commands:")
                print("cilium bgp peers")
                print("docker exec -it frr_router vtysh -c 'show bgp summary'")
                print("route -n")
                print("\n")

        if CONFIG_JSON['service_mesh']["driver"] == "cilium":
            print("# Test SPIRE Health")
            print("cilium status")
            print("kubectl exec -n cilium-spire spire-server-0 -c spire-server -- /opt/spire/bin/spire-server healthcheck")
            print("kubectl exec -n cilium-spire spire-server-0 -c spire-server -- /opt/spire/bin/spire-server agent list")
            print("kubectl exec -n cilium-spire spire-server-0 -c spire-server -- /opt/spire/bin/spire-server entry show -parentID spiffe://spiffe.cilium/ns/cilium-spire/sa/spire-agent")
            print("kubectl get ciliumidentities")
            print("kubectl exec -n cilium-spire spire-server-0 -c spire-server -- /opt/spire/bin/spire-server entry show -selector cilium:mutual-auth")
            print("\n")

        if CONFIG_JSON['registry']['enabled'] == "true":
            print("# Add registry as insecure:")
            print('#\t/etc/docker/daemon.json: ')
            REGISTRY_IP = get_docker_registry_ip()
            print('#\t\t { "insecure-registries": [ "%s:5000" ] }\n#' % REGISTRY_IP)

    print("#############################################################################")