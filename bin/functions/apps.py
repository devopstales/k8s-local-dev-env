#!/usr/bin/env python3

from .helepers import (
    which,
    run_command_stdout
)

#############################################################################
# Variables
#############################################################################

from .helepers import CONFIG_JSON, APPHOME

PROMETHEUS_HELMFILE_PATH = APPHOME + "/apps/crd/prometheus.yaml"

if CONFIG_JSON['monitoring']['enabled'] == "true":
    CM_TYPE="environment=monitoring"
else:
    CM_TYPE="environment=simple"

#############################################################################
# CRD
#############################################################################

def deploy_crds():
    print("# Install CRDs")
    # KUBECTL_PATH = which("kubectl")
    # run_command_stdout(RUN_KUBECTL)

    HELMFILE_PATH = which("helmfile")
    RUN_COMMAND = HELMFILE_PATH + " apply -q -f " + PROMETHEUS_HELMFILE_PATH
    run_command_stdout(RUN_COMMAND)

#############################################################################
# Monitoring
#############################################################################

def deploy_prometheus():
    NotImplemented

#############################################################################
# Kyverno
#############################################################################

#############################################################################
# Vault
#############################################################################

#############################################################################
# Keycloak SSO
#############################################################################

def create_sso_server():
    HELMFILE_PATH = which("helmfile")
    KUBECTL_PATH = which("kubectl")
    print("# Install Keycloak server")

    RUN_KUBECTL = KUBECTL_PATH + " apply -f " + APPHOME + "/apps/sso/ns.yaml"
    run_command_stdout(RUN_KUBECTL)

    RUN_COMMAND = HELMFILE_PATH + "  apply -q -f  " + APPHOME + "/apps/sso/sso.yaml" + " -l " + CM_TYPE
    run_command_stdout(RUN_COMMAND)

#############################################################################
# KubeDash
#############################################################################

def create_kubedash_server():
    HELMFILE_PATH = which("helmfile")
    print("# Install KubeDash server")

    RUN_COMMAND = HELMFILE_PATH + "  apply -q -f  " + APPHOME + "/apps/kubedash/kubedash.yaml" + " -l " + CM_TYPE
    run_command_stdout(RUN_COMMAND)

def remove_kubedash_server():
    HELMFILE_PATH = which("helmfile")
    print("# Install KubeDash server")

    RUN_COMMAND = HELMFILE_PATH + "  delete -q -f  " + APPHOME + "/apps/kubedash/kubedash.yaml" + " -l " + CM_TYPE
    run_command_stdout(RUN_COMMAND)