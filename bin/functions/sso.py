#!/usr/bin/env python3


from .helepers import (
    which,
    run_command_stdout, 
    APPHOME,
)

def create_sso_server():
    HELMFILE_PATH = which("helmfile")
    KUBECTL_PATH = which("kubectl")
    print("# Install Kewycloak server")

    RUN_KUBECTL = KUBECTL_PATH + " apply -f " + APPHOME + "/apps/sso/ns.yaml"
    run_command_stdout(RUN_KUBECTL)

    RUN_COMMAND = HELMFILE_PATH + "  apply -f  " + APPHOME + "/apps/sso/sso.yaml"
    run_command_stdout(RUN_COMMAND)