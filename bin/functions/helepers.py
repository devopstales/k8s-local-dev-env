#!/usr/bin/env python3

import platform
import configparser, json
import shutil
import os, trustme, subprocess

from pathlib import Path

HOME = str(Path.home())
APPHOME = HOME + "/k8s-local-dev-env"
ROOT_CERT_PATH = APPHOME + "/.certs/kdev_rootCA.crt"
ROOT_KEY_PATH = APPHOME + "/.certs/kdev_rootCA.key"
APP_PAM_PATH = APPHOME + "/.certs/kdev_app.pem"
APP_KEY_PATH = APPHOME + "/.certs/kdev_app.key"
APP_CERT_PATH = APPHOME + "/.certs/kdev_app.crt"

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
    else:
        if CONFIG_JSON['general']['logging'] == "DEBUG":
            print(result.stdout)

    if result.returncode != 0:
        exit(result.returncode)

#############################################################################
## Dependency tests
#############################################################################

def which(program):
    path = shutil.which(program) 

    if path is None:
        print(f"no executable found for command {program}")
        exit(1)
    else:
        return path

def kernel_dodule_test(modules):
    if platform.system() != 'Darwin':
        import kmodule
        mlist = kmodule.lsmod ()
        for m in modules:
            is_module = False

            for m, v in mlist.items ():
                if v.name == m:
                    is_module = True

            if not is_module:
                kmodule.insmod (m)
        print("# Kernel modules are loaded")

def dependency_test(DEPENDENCIES, KERNEL_MODULES):
    for BIN in DEPENDENCIES:
        which(BIN)
    print("# Dependencies tested")
    kernel_dodule_test(KERNEL_MODULES)

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
            identities="*.kdev.intra",
            organization_name="kdev",
            organization_unit_name="IT",
            key_type=trustme.KeyType(0)
        )

        # static files
        ca.cert_pem.write_to_path(ROOT_CERT_PATH)
        ca.private_key_pem.write_to_path(ROOT_KEY_PATH)

        app_cert.private_key_and_cert_chain_pem.write_to_path(APP_PAM_PATH)
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
        

def manage_cert():
    get_cert()
