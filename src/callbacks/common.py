from . import callback_next, callback_prev
import tg


def handle_callback(command, chat, message, callback, db_conn, token):
    if command.startswith("/next"):
        section_hash = command.removeprefix("/next@")
        callback_next.handle(section_hash=section_hash,
                             chat=chat,
                             message=message,
                             db_conn=db_conn,
                             token=token)
    if command.startswith("/prev"):
        section_hash = command.removeprefix("/prev@")
        callback_prev.handle(section_hash=section_hash,
                             chat=chat,
                             message=message,
                             db_conn=db_conn,
                             token=token)
    if command.startswith("/subscribe"):
        tg.answer_callback(token=token, callback=callback, text='YOU ARE SUBSCRIBED')
        # callback_prev.handle(section_hash=section_hash,
        #                      chat=chat,
        #                      message=message,
        #                      db_conn=db_conn,
        #                      token=token)
