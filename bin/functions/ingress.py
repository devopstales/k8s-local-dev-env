#!/usr/bin/env python3

from .helepers import (
    which,
    run_command_stdout, 
    CONFIG_JSON, 
    APPHOME,
    ROOT_CERT_PATH,
    ROOT_KEY_PATH,
)

#############################################################################
# Variables
#############################################################################

INGRESS_TYPE = CONFIG_JSON['ingress']['driver']
if INGRESS_TYPE == "nginx":
    INGRESS_HELMFILE_PATH = APPHOME + "/apps/ingress_nginx/nginx.yaml"
elif INGRESS_TYPE == "pomerium":
    INGRESS_HELMFILE_PATH = APPHOME + "/apps/ingress_pomerium/pomerium.yaml"

if CONFIG_JSON['network']['loadbalancer'] == "cilium":
    if CONFIG_JSON['monitoring']['enabled'] == "true":
        INGRES_TYPE="environment=loadbalancer-monitoring"
    else:
        INGRES_TYPE="environment=loadbalancer"
else:
    if CONFIG_JSON['monitoring']['enabled'] == "true":
        INGRES_TYPE="environment=nodeport-monitoring"
    else:
        INGRES_TYPE="environment=nodeport"


CM_HELMFILE_PATH =  APPHOME + "/apps/cert_manager/cert_manager.yaml"
ISSUER_PATH = APPHOME + "/apps/cert_manager/cert_manager-issuer.yaml"
if CONFIG_JSON['monitoring']['enabled'] == "true":
    if CONFIG_JSON['ingress']['apigateway'] == "none":
        CM_TYPE="environment=monitoring"
    else:
        CM_TYPE="environment=monitoring-ga"
else:
    if CONFIG_JSON['ingress']['apigateway'] == "none":
        CM_TYPE="environment=simple"
    else:
        CM_TYPE="environment=simple-ga"


#############################################################################
# Ingress controller
#############################################################################

def install_ingress():
    if INGRESS_TYPE == "nginx" or INGRESS_TYPE == "pomerium":
        HELMFILE_PATH = which("helmfile")
        RUN_COMMAND = HELMFILE_PATH + " apply -f " + INGRESS_HELMFILE_PATH + " -l " + INGRES_TYPE
        print("# Install Ingress Controller")
        run_command_stdout(RUN_COMMAND)

def remove_ingress():
    if INGRESS_TYPE == "nginx" or INGRESS_TYPE == "pomerium":
        HELMFILE_PATH = which("helmfile")
        RUN_COMMAND = HELMFILE_PATH + " destroy -f " + INGRESS_HELMFILE_PATH + " -l " + INGRES_TYPE
        print("# Remove Ingress Controller")
        run_command_stdout(RUN_COMMAND)

#############################################################################
# Cert Manager
#############################################################################

def install_cert_manager():
    HELMFILE_PATH = which("helmfile")
    RUN_COMMAND = HELMFILE_PATH + " apply -f " + CM_HELMFILE_PATH + " -l " + CM_TYPE
    print("# Install cert-manager")
    run_command_stdout(RUN_COMMAND)

    KUBECTL_PATH = which("kubectl")
    RUN_KUBECTL = KUBECTL_PATH + f" create secret tls ca-key-pair --cert={ROOT_CERT_PATH} --key={ROOT_KEY_PATH} -n ingress-system"
    run_command_stdout(RUN_KUBECTL)
    RUN_KUBECTL = KUBECTL_PATH + " apply -n ingress-system -f " + ISSUER_PATH
    run_command_stdout(RUN_KUBECTL)

def remove_cert_manager():
    print("# Remove cert-manager")

    KUBECTL_PATH = which("kubectl")

    RUN_KUBECTL = KUBECTL_PATH + " delete -n ingress-system -f " + ISSUER_PATH
    run_command_stdout(RUN_KUBECTL)

    RUN_KUBECTL = KUBECTL_PATH + " delete -n ingress-system secret ca-key-pair"
    run_command_stdout(RUN_KUBECTL)

    HELMFILE_PATH = which("helmfile")
    RUN_COMMAND = HELMFILE_PATH + " destroy -f " + CM_HELMFILE_PATH + " -l " + CM_TYPE
    run_command_stdout(RUN_COMMAND)

