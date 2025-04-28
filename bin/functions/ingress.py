#!/usr/bin/env python3

from .helepers import which, run_command_stdout

#############################################################################
# Variables
#############################################################################

from .helepers import CONFIG_JSON, APPHOME, ROOT_CERT_PATH, ROOT_KEY_PATH

INGRESS_TYPE_LIST = ["nginx", "pomerium"]

INGRESS_TYPE = CONFIG_JSON['ingress']['driver']

if CONFIG_JSON['sso']['enabled'] != "true":
    print("# SSO is not enabled. Installing Nginx Ingress controller")
    INGRESS_TYPE = "nginx"
    
if CONFIG_JSON['network']['driver'] == "cilium-helm":
    if CONFIG_JSON['network']['loadbalancer'] == "cilium":
        if CONFIG_JSON['monitoring']['enabled'] == "true":
            INGRESS_LABEL="environment=loadbalancer-monitoring"
        else:
            INGRESS_LABEL="environment=loadbalancer"
else:
    if CONFIG_JSON['monitoring']['enabled'] == "true":
        INGRESS_LABEL="environment=nodeport-monitoring"
    else:
        INGRESS_LABEL="environment=nodeport"

POMERIUM_ISSUER_PATH = APPHOME + "/apps/ingress_pomerium/pomerium-cert.yaml"


CM_HELMFILE_PATH =  APPHOME + "/apps/cert_manager/cert_manager.yaml"
TM_HELMFILE_PATH = APPHOME + "/apps/cluster_system/trust_manager.yaml"
CAI_HELMFILE_PATH = APPHOME + "/apps/cluster_system/ca_injector.yaml"

REFLECTOR_HELMFILE_PATH = APPHOME + "/apps/cluster_system/reflector.yaml"
BUNDLE_PATH = APPHOME + "/apps/cluster_system/trust_manager-bundle.yaml"

ISSUER_PATH = APPHOME + "/apps/cert_manager/cert_manager-issuer.yaml"
if CONFIG_JSON['monitoring']['enabled'] == "true":
    TM_TYPE="environment=monitoring"
    if CONFIG_JSON['service_mesh']['apigateway'] == "none":
        CM_TYPE="environment=monitoring"
    else:
        CM_TYPE="environment=monitoring-ga"
else:
    TM_TYPE="environment=simple"
    if CONFIG_JSON['service_mesh']['apigateway'] == "none":
        CM_TYPE="environment=simple"
    else:
        CM_TYPE="environment=simple-ga"


#############################################################################
# Ingress controller
#############################################################################

def install_ingress():
    HELMFILE_PATH = which("helmfile")
    KUBECTL_PATH = which("kubectl")
    MINIKUBE_PATH = which("minikube")

    if INGRESS_TYPE in INGRESS_TYPE_LIST:          
        if INGRESS_TYPE == "nginx":
            if CONFIG_JSON['network']['driver'] == "cilium-helm" \
                and CONFIG_JSON['network']['loadbalancer'] == "cilium":
                    INGRESS_HELMFILE_PATH = APPHOME + "/apps/ingress_nginx/nginx.yaml"
                    
                    RUN_COMMAND = HELMFILE_PATH + " apply -q -f " + INGRESS_HELMFILE_PATH + " -l " + INGRESS_LABEL
                    print("# Install Ingress Controller")
                    run_command_stdout(RUN_COMMAND)
            else:
                MINIKUBE_COMMAND = MINIKUBE_PATH + " -p kdev addons enable ingress"
                print("# Install Ingress Controller")
                run_command_stdout(MINIKUBE_COMMAND)
            
        elif INGRESS_TYPE == "pomerium":
            INGRESS_HELMFILE_PATH = APPHOME + "/apps/ingress_pomerium/pomerium.yaml"

            RUN_KUBECTL = KUBECTL_PATH + f" apply -f " + POMERIUM_ISSUER_PATH
            run_command_stdout(RUN_KUBECTL)
    
            RUN_COMMAND = HELMFILE_PATH + " apply -q -f " + INGRESS_HELMFILE_PATH + " -l " + INGRESS_LABEL
            print("# Install Ingress Controller")
            run_command_stdout(RUN_COMMAND)

def remove_ingress():
    if INGRESS_TYPE in INGRESS_TYPE_LIST:
        if INGRESS_TYPE == "nginx":
            INGRESS_HELMFILE_PATH = APPHOME + "/apps/ingress_nginx/nginx.yaml"

        elif INGRESS_TYPE == "pomerium":
            INGRESS_HELMFILE_PATH = APPHOME + "/apps/ingress_pomerium/pomerium.yaml"
        
        HELMFILE_PATH = which("helmfile")
        RUN_COMMAND = HELMFILE_PATH + " destroy -q -f " + INGRESS_HELMFILE_PATH + " -l " + INGRESS_LABEL
        print("# Remove Ingress Controller")
        run_command_stdout(RUN_COMMAND)

#############################################################################
# Cert Manager
#############################################################################

def install_cert_manager():
    HELMFILE_PATH = which("helmfile")
    RUN_COMMAND = HELMFILE_PATH + " apply -q -f " + CM_HELMFILE_PATH + " -l " + CM_TYPE
    print("# Install cert-manager")
    run_command_stdout(RUN_COMMAND)
    
    print("## Install reflector")
    RUN_COMMAND = HELMFILE_PATH + " apply -q -f " + REFLECTOR_HELMFILE_PATH
    run_command_stdout(RUN_COMMAND)

    print("## Trust Manager")
    RUN_COMMAND = HELMFILE_PATH + " apply -q -f " + TM_HELMFILE_PATH + " -l " + TM_TYPE
    run_command_stdout(RUN_COMMAND)

    print("## CA Injector")
    RUN_COMMAND = HELMFILE_PATH + " apply -q -f " + CAI_HELMFILE_PATH + " -l " + TM_TYPE
    run_command_stdout(RUN_COMMAND)

    print("## CA, Cert Bundle, Issuers")
    KUBECTL_PATH = which("kubectl")
    RUN_KUBECTL = KUBECTL_PATH + f" create secret generic ca-key-pair --from-file=ca.crt={ROOT_CERT_PATH} --from-file=tls.crt={ROOT_CERT_PATH} --from-file=tls.key={ROOT_KEY_PATH} -n ingress-system"
    run_command_stdout(RUN_KUBECTL)
    RUN_KUBECTL = KUBECTL_PATH + f" annotate secret ca-key-pair -n ingress-system reflector.v1.k8s.emberstack.com/reflection-allowed=true reflector.v1.k8s.emberstack.com/reflection-auto-enabled=true"
    run_command_stdout(RUN_KUBECTL)
    RUN_KUBECTL = KUBECTL_PATH + " apply -n ingress-system -f " + ISSUER_PATH
    run_command_stdout(RUN_KUBECTL)
    RUN_KUBECTL = KUBECTL_PATH + " apply -n cluster-system -f " + BUNDLE_PATH
    run_command_stdout(RUN_KUBECTL)


def remove_cert_manager():
    print("# Remove cert-manager")

    KUBECTL_PATH = which("kubectl")

    RUN_KUBECTL = KUBECTL_PATH + " delete -n ingress-system -f " + ISSUER_PATH
    run_command_stdout(RUN_KUBECTL)

    RUN_KUBECTL = KUBECTL_PATH + " delete -n ingress-system secret ca-key-pair"
    run_command_stdout(RUN_KUBECTL)

    HELMFILE_PATH = which("helmfile")
    RUN_COMMAND = HELMFILE_PATH + " destroy -q -f " + CM_HELMFILE_PATH + " -l " + CM_TYPE
    run_command_stdout(RUN_COMMAND)

