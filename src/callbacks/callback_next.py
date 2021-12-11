import logging

import tg


def handle(token, chat, message, db_conn, section):
    logging.info("Processing /next: (chat: {}, section: {})".format(
        chat, section))

    data = db_conn.get('{}:data'.format(section))
    if data:
        data = data.decode('utf-8')
        keyboard = make_data_keyboard(section)
        tg.edit_message(token=token,
                        chat=chat,
                        message=message,
                        text=data,
                        keyboard=keyboard)
    else:
        next_sections = db_conn.smembers('{}:next'.format(section))
        keyboard = make_keyboard(section, next_sections)
        tg.edit_message(token=token,
                        chat=chat,
                        message=message,
                        text=section,
                        keyboard=keyboard)


def make_data_keyboard(current_section):
    keyboard = []

    action_buttons = [
        {
            'text': '\U00002b05',
            'callback_data': '/prev@{}'.format(current_section)
        },
        {
            'text': '\U0001f514',
            'callback_data': '/subscribe@{}'.format(current_section)
        },
        {
            'text': '\U0001f515',
            'callback_data': '/unsubscribe@{}'.format(current_section)
        },
        {
            'text': '\U0001f4e3',
            'callback_data': '/proposal@{}'.format(current_section)
        },
    ]

    keyboard.append(action_buttons)

    return keyboard


def make_keyboard(current_section, next_sections):
    keyboard = []

    for next_section in next_sections:
        next_section = next_section.decode('utf-8')
        next_section_path = "{}/{}".format(current_section, next_section)
        button = [{
            'text': next_section,
            'callback_data': '/next@{}'.format(next_section_path)
        }]
        keyboard.append(button)

    action_buttons = [
        {
            'text': '\U00002b05',
            'callback_data': '/prev@{}'.format(current_section)
        },
        {
            'text': '\U0001f514',
            'callback_data': '/subscribe@{}'.format(current_section)
        },
        {
            'text': '\U0001f515',
            'callback_data': '/unsubscribe@{}'.format(current_section)
        },
        {
            'text': '\U0001f4e3',
            'callback_data': '/proposal@{}'.format(current_section)
        },
    ]

    keyboard.append(action_buttons)

    return keyboard
