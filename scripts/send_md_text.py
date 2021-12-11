import argparse
import requests
import argparse
import sys
import logging, logging.config

argparser = argparse.ArgumentParser()
argparser.add_argument("--chat", type=str, required=True)
argparser.add_argument("--data", type=str, required=True)
argparser.add_argument("--token", type=str, required=True)
args = argparser.parse_args()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    data = open(args.data).read()

    url = "https://api.telegram.org/bot{}/sendMessage".format(args.token)
    request_body = {
        'chat_id': args.chat,
        'text': data,
        'parse_mode': 'Markdown'
    }

    logging.debug("[TG.SEND_MESSAGE] BODY: {}".format(request_body))
    response = requests.post(url, json=request_body)
    if response.status_code == 200:
        response_body = response.json()
        if not response_body['ok']:
            logging.error("Telegram call failed: {}".format(response_body))
    else:
        logging.error("Telegram call failed: (reason: {}, details: {})".format(
            response.reason, response.json()))


if __name__ == "__main__":
    main()
