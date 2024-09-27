#!/usr/bin/env python3


from .helepers import (
    which,
    run_command_stdout, 
    CONFIG_JSON, 
    APPHOME,
)

def create_dns_server():
    HELMFILE_PATH = which("helmfile")
    KUBECTL_PATH = which("kubectl")
    print("# Install DNS server")

    RUN_KUBECTL = KUBECTL_PATH + " apply -f " + APPHOME + "/apps/cluster_system/ns.yaml"
    run_command_stdout(RUN_KUBECTL)

    RUN_COMMAND = HELMFILE_PATH + "  apply -f  " + APPHOME + "/apps/cluster_system/etcd.yaml"
    run_command_stdout(RUN_COMMAND)

    RUN_COMMAND = HELMFILE_PATH + "  apply -f  " + APPHOME + "/apps/cluster_system/coredns.yaml"
    run_command_stdout(RUN_COMMAND)

    RUN_COMMAND = HELMFILE_PATH + "  apply -f  " + APPHOME + "/apps/cluster_system/external-dns.yaml"
    run_command_stdout(RUN_COMMAND)
