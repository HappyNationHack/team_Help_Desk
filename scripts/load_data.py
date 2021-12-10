import argparse
import sys
import os, os.path
import redis
import argparse
import logging, logging.config

argparser = argparse.ArgumentParser()
argparser.add_argument("--data", type=str, required=True)
argparser.add_argument("--db-host", type=str, required=True)
argparser.add_argument("--db-port", type=int, required=True)
args = argparser.parse_args()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    db_conn = redis.Redis(host=args.db_host, port=args.db_port, db=0)
    set_root_segments(args.data, db_conn)
    for dir in os.listdir(args.data):
        process_data_segment(args.data, dir, db_conn)


def set_root_segments(data_path, db_conn):
    root_dirs = os.listdir(data_path)
    logging.debug("Setting root dirs: {}".format(root_dirs))
    db_conn.sadd("/root", *root_dirs)


def process_data_segment(data_root, data_path, db_conn):
    logging.debug("Processing data entry {}".format(data_path))
    data_entries = os.listdir(os.path.join(data_root, data_path))
    if data_entries == ["_data"]:
        logging.debug("Saving data for entry {}".format(data_path))
        db_conn.set("{}:data".format(data_path),
                    open(os.path.join(data_root, data_path, "_data")).read())
    else:
        logging.debug("Setting data child entries {}".format(data_entries))
        db_conn.sadd("{}:next".format(data_path), *data_entries)
        for entry in os.listdir(os.path.join(data_root, data_path)):
            new_data_path = os.path.join(data_path, entry)
            process_data_segment(data_root, new_data_path, db_conn)


if __name__ == "__main__":
    main()
