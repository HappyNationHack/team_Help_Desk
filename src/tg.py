import requests
import logging
import json


def getUpdates(token, offset):
    url = "https://api.telegram.org/bot{}/getUpdates".format(token)
    params = {"offset": offset, "allowed_updates": json.dumps(["message"])}
    response = requests.get(url=url, params=params)

    if response.status_code == 200:
        response_body = response.json()
        if response_body['ok']:
            return response_body['result']
        else:
            logging.error("Telegram call failed: {}".format(response_body))
    else:
        logging.error("Telegram call failed: {}".format(response.reason))
