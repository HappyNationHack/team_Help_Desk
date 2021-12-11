from . import command_list


def handle_command(command, chat, db_conn, token):
    if command == "/list":
        command_list.handle(chat=chat, db_conn=db_conn, token=token)
