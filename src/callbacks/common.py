from . import callback_next, callback_prev


def handle_callback(command, chat, message, db_conn, token):
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
