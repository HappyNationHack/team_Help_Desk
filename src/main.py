import argparse
import yaml
import time
import sys
import logging, logging.config

import tg

argparser = argparse.ArgumentParser()
argparser.add_argument("--config", type=str, required=True)
argparser.add_argument("--token", type=str, required=True)
args = argparser.parse_args()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    config = load_config(args.config)
    logging.info("Starting with config: {}".format(config))
    loop(config, args.token)


def loop(config, token):
    loop_interval = config.get('loop_interval')
    logging.info("Starting main loop with {}s interval".format(loop_interval))

    offset = 0  # update offset with update id
    while True:
        time.sleep(loop_interval)

        updates = tg.getUpdates(token, offset)
        if updates:
            logging.info("Processing {} update(s)".format(len(updates)))
            for update in updates:
                logging.debug("Processing update: {}".format(update))
                update_id = update['update_id']
                if update_id >= offset:
                    offset = update_id + 1


def load_config(config_path):
    logging.info("Loading config from {}".format(config_path))
    with open(config_path, "r") as config:
        return yaml.load(config, yaml.Loader)


if __name__ == "__main__":
    main()
