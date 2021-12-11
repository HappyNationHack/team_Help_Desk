import argparse
import yaml
import time
import sys
import redis
import logging, logging.config

import tg
from commands.common import handle_command
from callbacks.common import handle_callback

argparser = argparse.ArgumentParser()
argparser.add_argument("--config", type=str, required=True)
argparser.add_argument("--token", type=str, required=True)
args = argparser.parse_args()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    config = load_config(args.config)
    logging.info("Starting with config: {}".format(config))

    db_conn = redis.Redis(host=config['db']['host'], port=config['db']['port'])

    loop(config, args.token, db_conn)


def loop(config, token, db_conn):
    loop_interval = config.get('loop_interval')
    logging.info("Starting main loop with {}s interval".format(loop_interval))

    offset = 0  # update offset with update id
    while True:
        time.sleep(loop_interval)

        updates = tg.get_updates(token, offset)
        if updates:
            logging.info("Processing {} update(s)".format(len(updates)))
            for update in updates:
                logging.debug("Processing update: {}".format(update))
                update_id = update['update_id']
                if update_id >= offset:
                    offset = update_id + 1

                if 'message' in update:
                    command = update['message']['text']
                    chat = update['message']['chat']['id']
                    handle_command(command=command,
                                   chat=chat,
                                   db_conn=db_conn,
                                   token=token)
                elif 'callback_query' in update:
                    command = update['callback_query']['data']
                    chat = update['callback_query']['message']['chat']['id']
                    message = update['callback_query']['message']['message_id']
                    handle_callback(command=command,
                                    chat=chat,
                                    message=message,
                                    db_conn=db_conn,
                                    token=token)


def load_config(config_path):
    logging.info("Loading config from {}".format(config_path))
    with open(config_path, "r") as config:
        return yaml.load(config, yaml.Loader)


if __name__ == "__main__":
    main()
