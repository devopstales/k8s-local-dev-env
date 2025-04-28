#!/usr/bin/env python3

import platform
import configparser, json
import shutil
import os, trustme, subprocess

from pathlib import Path

#############################################################################
## Variables
#############################################################################

HOME = str(Path.home())
APPHOME = HOME + "/k8s-local-dev-env"

ROOT_PEM_NAME = "/kdev_rootCA.pem"
ROOT_CERT_PATH = APPHOME + "/.certs" + ROOT_PEM_NAME
ROOT_KEY_PATH = APPHOME + "/.certs/kdev_rootCA.key"
APP_PEM_PATH = APPHOME + "/.certs/kdev_app.pem"
APP_KEY_PATH = APPHOME + "/.certs/kdev_app.key"
APP_CERT_PATH = APPHOME + "/.certs/kdev_app.crt"

MINIKUBE_CERT_FOLDER = HOME + "/.minikube/certs"
MINIKUBE_CERT_PATH = MINIKUBE_CERT_FOLDER + "/ca.pem"
MINIKUBE_KEY_PATH = MINIKUBE_CERT_FOLDER + "/ca-key.pem"


#############################################################################
## Config
#############################################################################

def read_config():
    config_object = configparser.ConfigParser()
    config_object.read(APPHOME + '/config.ini')

    output_dict=dict()
    sections=config_object.sections()

    for section in sections:
        items=config_object.items(section)
        output_dict[section]=dict(items)

    return output_dict

CONFIG_JSON = read_config()

if CONFIG_JSON['general']['logging'] == "DEBUG":
    print("# config:")
    print(CONFIG_JSON)

#############################################################################
## OS commands
#############################################################################

def run_command_stdout(*args):
    result = subprocess.run(args, capture_output=True, text=True, shell=True)

    if result.stderr:
        print(result.stderr)
    #else:
    #    if CONFIG_JSON['general']['logging'] == "DEBUG":
    #        print(result.stdout)

    if result.returncode != 0:
        exit(result.returncode)
        
def which(program):
    path = shutil.which(program) 

    if path is None:
        print(f"no executable found for command {program}")
        exit(1)
    else:
        return path
    
#############################################################################
## Cert Generation
#############################################################################

def get_cert():
    check_file = os.path.isfile(ROOT_CERT_PATH)
    if not check_file:
        ca = trustme.CA(
            organization_name="kdev",
            organization_unit_name="IT",
            path_length=0,
            key_type=trustme.KeyType(0)
        )
        app_cert = ca.issue_cert(
            "*.kdev.intra",
            organization_name="kdev",
            organization_unit_name="IT",
            key_type=trustme.KeyType(0)
        )

        # static files
        ca.cert_pem.write_to_path(ROOT_CERT_PATH)
        ca.private_key_pem.write_to_path(ROOT_KEY_PATH)

        app_cert.private_key_and_cert_chain_pem.write_to_path(APP_PEM_PATH)
        app_cert.cert_chain_pems[0].write_to_path(APP_CERT_PATH)
        app_cert.private_key_pem.write_to_path(APP_KEY_PATH)

        # Linux Trust
        # ca.cert_pem.write_to_path("/usr/local/share/ca-certificates/kdev_rootCA.crt")
        # sudo update-ca-certificates

        # Firefox trust
        #with codecs.open('/usr/lib/firefox/distribution/policies.json', 'r+', encoding='utf-8') as f:
        #    data = json.load(f)
        #    data['policies']['Certificates'] = {
        #        "ImportEnterpriseRoots": True,
        #            "Install": [
        #                    "/usr/local/share/ca-certificates/kdev_rootCA.crt",                            ]
        #    }
        #    f.seek(0)
        #    json.dump(data, f, indent=4)
        #    f.truncate()
        
    #check_folder = os.path.isdir(MINIKUBE_CERT_FOLDER)
    #if not check_folder:
    #    os.makedirs(MINIKUBE_CERT_FOLDER)
#
    #    shutil.copyfile(ROOT_CERT_PATH, MINIKUBE_CERT_PATH)
    #    shutil.copyfile(ROOT_KEY_PATH, MINIKUBE_KEY_PATH)
        
        

def manage_cert():
    get_cert()