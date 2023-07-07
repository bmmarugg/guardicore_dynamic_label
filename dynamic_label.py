#!/usr/bin/python3
# v1.0 | 2023-07-07

import json
import requests
import urllib3
from pprint import pprint

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base variables for important things. Helps make the script a little shorter.
base_doc_path = "/PATH/TO/FILE/DIRECTORY"
base_centra_url = "https://YOUR/URL/HERE/api/"


# JSON credential file path where your API username and password are stored.
with open(f"{base_doc_path}/creds.json") as creds:
    creds = json.load(creds)

username = creds['guardicore_user']
passwd = creds['guardicore_pass']


# Function that uses the API-privileged username and password to authenticate to Centra and pull a token that will be
# used for API calls.
def get_token():
    auth_url = f"https://{base_centra_url}/v3.0"

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


# The function that actually creates the label and assigns the dynamic criteria values.
def create_dyn_label(token):
    # New headers that includes the token obtained from the previous function
    headers = {
        "content-type": "application/json",
        "Authorization": f"bearer {token}"
    }

    # The file with the dynamic criteria VALUES to be added to the label.
    dyn_criteria_file = open(f"{base_doc_path}/dyn_criteria.txt", "r")

    # Lets the user put in their own key:value pair names each time the script is ran.
    label_key = input("Label Key: ")
    label_value = input("Label Value: ")

    # Iterates through the dyn_criteria.txt file and builds the data payload as a list that will be attached in the next
    # step.
    dyn_list = []
    for address in dyn_criteria_file:
        address = address.replace(" ", "")
        address = address.replace("\n", "")
        dyn_dict = {
            "field": "numeric_ip_addresses",
            "op": "SUBNET",
            "argument": f"{address}"
        }

        dyn_list.append(dyn_dict)

    # The next data payload that creates the label using the user-defined key:value pair and attaches the list of
    # dynamic criteria built above as the dynamic criteria.
    dyn_label = {
        "key": f"{label_key}",
        "value": f"{label_value}",
        "criteria": dyn_list
    }

    # The actual API call that sends the full data payload. It will print an ID code upon a successful POST call.
    pprint(requests.post(f"{base_centra_url}/v4.0/labels",
                         verify=False, headers=headers, data=json.dumps(dyn_label)).json())


create_dyn_label(token)
