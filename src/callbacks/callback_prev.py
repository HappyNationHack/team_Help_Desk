import logging

import tg


def handle(token, chat, message, db_conn, section):
    logging.info("Processing /prev: (chat: {}, section: {})".format(
        chat, section))

    prev_section = get_prev_section(section)

    keyboard = make_keyboard(section, prev_section, db_conn)
    tg.edit_message(token=token,
                    chat=chat,
                    message=message,
                    text=prev_section,
                    keyboard=keyboard)


def get_prev_section(section):
    segments = section.split("/")
    if len(segments) == 1:
        return "/root"
    else:
        return "/".join(segments[:-1])


def make_keyboard(current_section, prev_section, db_conn):
    keyboard = []

    # two db queries but i don't care it's hackathon
    same_level_sections = db_conn.smembers('/root')
    if not prev_section == "/root":
        same_level_sections = db_conn.smembers('{}:next'.format(prev_section))

    print(prev_section, same_level_sections)

    for section in same_level_sections:
        section = section.decode('utf-8')

        section_path = section
        if not prev_section == "/root":
            section_path = "{}/{}".format(prev_section, section)

        button = [{
            'text': section,
            'callback_data': '/next@{}'.format(section_path)
        }]
        keyboard.append(button)

    action_buttons = [
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

    if not prev_section == "/root":
        action_buttons.insert(0, {
            'text': '\U00002b05',
            'callback_data': '/prev@{}'.format(prev_section)
        })

    keyboard.append(action_buttons)

    return keyboard
