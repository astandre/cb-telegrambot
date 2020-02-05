from requests import Session
import requests
import os

BASE_URL = "http://127.0.0.1:5005"
CONNECTION_KEY = "tokendeseguridad"
session = Session()
session.trust_env = False
session.verify = False
session.headers["Accept"] = "application/json"
session.headers["Content-Type"] = "application/json"


def get_greetings():
    url = BASE_URL + "/about/agent"
    try:
        r = session.get(url, json={"token": CONNECTION_KEY})
        if r.status_code == 200:
            response = r.json()
            # print(response)
            return response
    except requests.exceptions.RequestException as e:
        print(e)


def chat_with_system(data):
    url = BASE_URL + "/chat"
    json = {"token": CONNECTION_KEY}
    json.update(data)
    try:
        r = session.post(url, json=json)
        print(">>>>> SentData ", url, json)
        if r.status_code == 200:
            response = r.json()
            print("<<<<< ReceivedData ", response)
            return response
    except requests.exceptions.RequestException as e:
        print(e)
