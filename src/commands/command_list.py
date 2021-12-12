import logging
from hashlib import md5

import tg


def handle(token, chat, db_conn):
    logging.info("Processing /list: (chat: {})".format(chat))
    root_sections = db_conn.smembers("/root")
    keyboard = make_keyboard(root_sections)
    tg.send_message(token=token, chat=chat, text="test", keyboard=keyboard)


def make_keyboard(sections):
    keyboard = []

    for section in sections:
        hash = md5(section).hexdigest()
        button = [{
            'text': section.decode('utf-8'),
            'callback_data': '/next@{}'.format(hash)
        }]
        keyboard.append(button)

    action_buttons = [
        {
            'text': '\U0001f514',
            'callback_data': '/subscribe@{}'.format('/root')
        },
        # {
        #     'text': '\U0001f515',
        #     'callback_data': '/unsubscribe@{}'.format('/root')
        # },
        {
            'text': '\U0001f4dd',
            'callback_data': '/edit@{}'.format('/root')
        },
    ]

    keyboard.append(action_buttons)

    return keyboard
