#!/usr/bin/env python3

from .helepers import (
    which,
    run_command_stdout
)

#############################################################################
## Variables
#############################################################################

MINIKUBE_PATH = which("minikube")
from .helepers import CONFIG_JSON
AUTH_CONFIG = ""

#############################################################################
## Functions
#############################################################################

def start_minikube(CNI_DRIVER):
    if CONFIG_JSON['sso']['enabled'] == 'true':
        AUTH_CONFIG = " --extra-config=apiserver.authorization-mode=Node,RBAC --extra-config=apiserver.oidc-issuer-url=https://keycloak.kdev.intra --extra-config=apiserver.oidc-username-claim=email --extra-config=apiserver.oidc-client-id=k8s"
        #AUTH_CONFIG = ' --extra-config=apiserver.authorization-mode=Node,RBAC --extra-config=apiserver.oidc-issuer-url="https://dev-sntb3oobjdasu742.eu.auth0.com/.well-known/openid-configuration" --extra-config=apiserver.oidc-client-id=iDYLn69xPnHUAJ7ysxUQASZxJwhuT33G --extra-config=apiserver.oidc-username-claim=nickname'
  
    RUN_COMMAND = MINIKUBE_PATH + " -p kdev start --cni=" + CNI_DRIVER + \
        " --driver=docker --network=kdev --embed-certs" + \
        AUTH_CONFIG
        #" --addons=metrics-server,volumesnapshots,csi-hostpath-driver" + \
        # --registry-mirror=http://198.18.254.1:5000 --insecure-registry=198.18.254.1:5000 --cache-images=true
        # --ports nat port
    print("# Start minikube cluster")
    run_command_stdout(RUN_COMMAND)

def stop_minikube():
    RUN_COMMAND = MINIKUBE_PATH + " -p kdev stop"
    print("# Stop minikube cluster")
    run_command_stdout(RUN_COMMAND)

def delete_minikube():
    RUN_COMMAND = MINIKUBE_PATH + " -p kdev delete"
    print("# Delete minikube cluster")
    run_command_stdout(RUN_COMMAND)
    
def pause_minikube():
    RUN_COMMAND = MINIKUBE_PATH + " -p kdev pause"
    print("# Pause minikube cluster")
    run_command_stdout(RUN_COMMAND)

def load_docker_image(image_name):
    RUN_COMMAND = MINIKUBE_PATH + " -p kdev image load " + image_name
    print("# Loading docker image: %s" % image_name)
    run_command_stdout(RUN_COMMAND)
    

def start_registry():
    RUN_COMMAND = MINIKUBE_PATH + " -p kdev addons enable registry"
    RUN_COMMAND2 = MINIKUBE_PATH + " -p kdev addons enable registry-aliases"
    print("# Start docker registry")
    run_command_stdout(RUN_COMMAND)
    run_command_stdout(RUN_COMMAND2)
    
def stop_registry():
    RUN_COMMAND = MINIKUBE_PATH + " -p kdev addons disable registry"
    print("# Stopdocker registry")
    run_command_stdout(RUN_COMMAND)