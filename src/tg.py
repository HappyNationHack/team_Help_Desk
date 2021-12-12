import requests
import logging
import json


def get_updates(token, offset):
    url = "https://api.telegram.org/bot{}/getUpdates".format(token)
    allowed_updates = json.dumps(["message", "callback_query"])
    params = {"offset": offset, "allowed_updates": allowed_updates}
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


def edit_message(token, chat, message, text, keyboard=None):
    url = "https://api.telegram.org/bot{}/editMessageText".format(token)
    request_body = {'chat_id': chat, 'message_id': message, 'text': text}
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

def answer_callback(token, callback, text=None):
    url = "https://api.telegram.org/bot{}/answerCallbackQuery".format(token)
    request_body = {'callback_query_id': callback, 'text': text}

    logging.debug("[TG.NSWER_CALLBACK_QUERY] BODY: {}".format(request_body))
    response = requests.post(url, json=request_body)
    if response.status_code == 200:
        response_body = response.json()
        if not response_body['ok']:
            logging.error("Telegram call failed: {}".format(response_body))
    else:
        logging.error("Telegram call failed: (reason: {}, details: {})".format(
            response.reason, response.json()))
