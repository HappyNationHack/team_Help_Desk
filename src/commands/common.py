from . import command_list, command_next


def handle_command(command, chat, db_conn, token):
    if command == "/list":
        command_list.handle(chat=chat, db_conn=db_conn, token=token)
    elif command.startswith("/next"):
        section = command.removeprefix("/next@")
        command_next.handle(section=section, chat=chat, db_conn=db_conn, token=token)
