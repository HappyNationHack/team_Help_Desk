import requests
import logging
import json


def get_updates(token, offset):
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


def send_message(token, chat, text, keyboard=None):
    url = "https://api.telegram.org/bot{}/sendMessage".format(token)
    request_body = {'chat_id': chat, 'text': text}
    if keyboard:
        request_body['reply_markup'] = json.dumps(
            {'inline_keyboard': keyboard})

    logging.debug("[TG.SEND_MESSAGE] BODY: {}".format(request_body))
    response = requests.post(url, json=request_body)
    if response.status_code == 200:
        response_body = response.json()
        if not response_body['ok']:
            logging.error("Telegram call failed: {}".format(response_body))
    else:
        logging.error("Telegram call failed: (reason: {}, details: {})".format(
            response.reason, response.json()))
