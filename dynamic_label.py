#!/usr/bin/python3
# v2.0 | 2023-09-29

import json
import requests
import urllib3
from pprint import pprint

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_doc_path = "PATH/TO/docs"
base_centra_url = "https://<YOUR-URL-HERE>/api/v4.0"


# JSON credential file path where your API token is stored.
with open(f"{base_doc_path}/creds.json") as creds:
    creds = json.load(creds)

username = creds['guardicore_user']
passwd = creds['guardicore_pass']

def get_token():
    auth_url = "https://<YOUR-URL-HERE>/api/v3.0"

    headers = {
        "content-type": "application/json"
    }

    token_req = {
        "username": f"{username}",
        "password": f"{passwd}"
    }

    token = requests.post(f"{auth_url}/authenticate",
                          verify=False, headers=headers, data=json.dumps(token_req)).json().get('access_token')
    return token

token = get_token()


def subnet_dyn_label():
    headers = {
        "content-type": "application/json",
        "Authorization": f"bearer {token}"
    }

    dyn_criteria_file = open(f"{base_doc_path}/dyn_criteria.txt", "r")

    label_key = input("Label Key: ")
    label_value = input("Label Value: ")

    dyn_list = []
    for criteria in dyn_criteria_file:
        criteria = criteria.replace(" ", "")
        criteria = criteria.replace("\n", "")
        dyn_dict = {
            "field": "numeric_ip_addresses",
            "op": "SUBNET",
            "argument": f"{criteria}"
        }

        dyn_list.append(dyn_dict)

    dyn_label = {
        "key": f"{label_key}",
        "value": f"{label_value}",
        "criteria": dyn_list
    }


    pprint(requests.post(f"{base_centra_url}/labels", verify=False, headers=headers, data=json.dumps(dyn_label)).json())


def host_dyn_label():
    headers = {
        "content-type": "application/json",
        "Authorization": f"bearer {token}"
    }

    dyn_criteria_file = open(f"{base_doc_path}/dyn_criteria.txt", "r")

    label_key = input("Label Key: ")
    label_value = input("Label Value: ")

    dyn_list = []
    for criteria in dyn_criteria_file:
        criteria = criteria.replace(" ", "")
        criteria = criteria.replace("\n", "")
        dyn_dict = {
            "field": "name",
            "op": "STARTSWITH",
            "argument": f"{criteria}"
        }

        dyn_list.append(dyn_dict)

    dyn_label = {
        "key": f"{label_key}",
        "value": f"{label_value}",
        "criteria": dyn_list
    }


    pprint(requests.post(f"{base_centra_url}/labels", verify=False, headers=headers, data=json.dumps(dyn_label)).json())

choice = input("Host or IP? \n")

if "ip" in choice.lower():
    subnet_dyn_label()

elif "host" in choice.lower():
    host_dyn_label()
