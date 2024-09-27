#!/usr/bin/env python3

from ..helepers import (
    which,
    run_command_stdout, 
    CONFIG_JSON, 
    APPHOME,
    ROOT_CERT_PATH,
    ROOT_KEY_PATH
)

PROMETHEUS_HELMFILE_PATH = APPHOME + "/crd/prometheus.yaml"

def deploy_crds():
    print("# Install CRDs")
    # KUBECTL_PATH = which("kubectl")
    # run_command_stdout(RUN_KUBECTL)

    HELMFILE_PATH = which("helmfile")
    RUN_COMMAND = HELMFILE_PATH + " apply -f " + PROMETHEUS_HELMFILE_PATH
    run_command_stdout(RUN_COMMAND)