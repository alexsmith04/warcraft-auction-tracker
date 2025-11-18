import requests
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('client_id')
CLIENT_SECRET = os.getenv('client_secret')

def get_access_token():
    url = "https://eu.battle.net/oauth/token"
    data = {"grant_type": "client_credentials"}
    resp = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    resp.raise_for_status()
    token = resp.json()["access_token"]
    return token

def get_commodities():
    token = get_access_token()
    url = "https://eu.api.blizzard.com/data/wow/auctions/commodities"
    params = {
        "namespace": "dynamic-eu",
        "locale": "en_US"
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }

    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()

def get_auctions_for_realm():
    token = get_access_token()
    
    # Id for Silvermoon
    connected_realm_id = 3391
    
    url = f"https://eu.api.blizzard.com/data/wow/connected-realm/{connected_realm_id}/auctions"
    params = {
        "namespace": "dynamic-eu",
        "locale": "en_US"
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }

    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()