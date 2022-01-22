import requests
import re
from collections import namedtuple
import time
import logging
import json
from argparse import ArgumentParser
import os
from datetime import datetime


api_status_url = "https://overpass-api.de/api/status"
api_url = "https://overpass-api.de/api/interpreter"

logging.basicConfig(level=logging.INFO)

ApiStatus = namedtuple("ApiStatus", ["rate_limit", "slots_available", "slot_timeouts"])

class NetworkError(Exception):
    pass

def get_api_status():
    # Send request
    resp = requests.get(api_status_url)
    if (resp.status_code != 200):
        logging.error("Unexpected status code (get_api_status) expected 200, got " + resp.status_code)
        raise NetworkError

    # Get the data
    data = resp.content.decode().split("\n")
    logging.debug(data)

    logging.info(data[0])

    # Parse
    slots_available = 0
    slot_timeouts = []
    for row in data:
        if row.startswith("Rate limit: "):
            rate_limit = int(row.split(":")[1])
        elif row.endswith("slots available now."):
            slots_available = int(row.split(" ")[0])
        elif row.startswith("Slot available after:"):
            match = re.search("in (\d+) seconds", row)
            if match is None:
                logging.warning("Weird api status response detected, retrying in 1s")
                time.sleep(1)
                return get_api_status()
            slot_timeout = int(match.group(1))
            slot_timeouts.append(slot_timeout)
    
    return ApiStatus(rate_limit, slots_available, slot_timeouts)


def print_status(status = None):
    rate_limit, slots_available, slot_timeouts = status or get_api_status()
    if len(slot_timeouts) == 0:
        logging.info("STATUS: %s/%s" % (slots_available, rate_limit))
    else:
        logging.info("STATUS: %s/%s (New %s in %s seconds)" % (
            slots_available, 
            rate_limit, 
            "slot" if len(slot_timeouts) == 1 else "slots", 
            slot_timeouts[0] if len(slot_timeouts) == 1 else slot_timeouts
        ))


def wait_for_free_slot(status = None, slots_needed = 1):
    status = status or get_api_status()
    rate_limit, slots_available, slot_timeouts = status
    if slots_needed > rate_limit:
        logging.error("Requested number of free slots is too large (Maximum: %s, Requested: %s)" % (rate_limit, slots_needed))
        raise AttributeError
    
    if slots_available >= slots_needed:
        return
    
    wait_time = sorted(slot_timeouts)[slots_needed-1] + 2       # Add 2 seconds just to be sure
    print_status(status)
    logging.info("Waiting for a free slot (%s seconds)" % wait_time)
    time.sleep(wait_time)


def get_split_count(query):
    match = re.search("/\* split_count=(\d+) \*/", query)
    return 0 if match == None else int(match.group(1))


def get_format(query):
    match = re.search(r"\[out:(\w+)[\(\]]", query)
    return "txt" if match == None else match.group(1)


def run_query(query, format="raw"):
    print_status()
    wait_for_free_slot()
    logging.info("Sending query")
    resp = requests.post(api_url, data=query)
    if format == "json":
        return json.loads(resp.content)["elements"]         # List
    elif format == "bytes":
        return resp.content
    else:
        return resp.content.decode()


def run_split_query(query, format="raw", partial_files_to_update=None):
    replace_pattern = r"\(x\s?,x\s?,x\s?,x\s?\)"

    split_count = get_split_count(query)
    if split_count == 0:
        yield 0, run_query(query, format)
    else:
        if len(re.findall(replace_pattern, query)) == 0:
            logging.error("split_count indicator found but no place for inserting the location (\"(x,x,x,x)\") found in the query.")
            raise AttributeError

        logging.info("Split query with %s parts started execution" % split_count)
        for i, send_request in zip(range(split_count), partial_files_to_update):
            if not send_request:
                logging.info("Skipping existing partial request %i" % i)
                continue

            start = i * 360 / split_count - 180
            end = 180 - (split_count-i-1) * 360 / split_count
            partial_query = re.sub(replace_pattern, "(-90, %s, 90, %s)" % (start, end), query)
            yield i, run_query(partial_query, format)

        logging.info("Split query finished execution")


def write_result(result, base_filename, frmt):
    filename = base_filename + "." + frmt
    logging.info("Writing (partial) result to %s" % filename)
    if frmt == "json":
        result = json.dumps(result, indent=4)
    
    with open(filename, "w" if type(result) == str else "wb", encoding="UTF-8") as fp:
        fp.write(result)


def get_partial_to_update(query_filename, base_filename, frmt, split_count, update):
    return [
        update or is_newer(query_filename, base_filename + "." + str(i) + "." + frmt)
        for i in range(split_count)
    ]


def combine_result_files(base_filename, frmt, split_count):
    with open(base_filename + "." + frmt, "w", encoding="UTF-8") as fp_out:
        for i in range(split_count):
            with open(base_filename + "." + str(i) + "." + frmt, "r", encoding="UTF-8") as fp_in:
                if frmt == "json":
                    json.dump(json.load(fp_in), fp_out, indent=4)
                elif frmt == "csv":
                    # Skip header for later files
                    if i == 0:
                        fp_out.write(fp_in.readline())
                        fp_out.write("\n")
                    else:
                        fp_in.readline()
                    
                    data = fp_in.read()
                    fp_out.write(data)
                    if len(data) > 0 and data[-1] != "\n":
                        fp_out.write("\n")
                else:
                    fp_out.write(fp_in.read())



def process(query, base_filename: str, query_filename, update):
    split_count = get_split_count(query)
    frmt = get_format(query)

    if split_count == 0:
        result = run_query(format=frmt)
        write_result(result, base_filename, frmt)
    else:
        partial_files_to_update = get_partial_to_update(query_filename, base_filename, frmt, split_count, update)
        result = [] if frmt == "json" else ""
        for i, partial_result in run_split_query(query, frmt, partial_files_to_update):
            if type(partial_result) == str and partial_result.startswith("<?xml"):
                logging.error("API server is not cooperative (returning an XML error), might be rate limited:")
                print(partial_result)
                print_status()
                logging.info("Stopping execution")
                exit(1)
            write_result(partial_result, base_filename + (".%s" % i), frmt)
        
        # Combine files
        combine_result_files(base_filename, frmt, split_count)


def get_file_mtime(filename):
    return os.path.getmtime(filename)

def is_newer(file_a, file_b):
    if os.path.exists(file_b):
        return get_file_mtime(file_a) > get_file_mtime(file_b)
    else:
        return True


def main(args):
    print_status()
    for file in args.query_files:
        with open(file, "r") as fp:
            query = fp.read()
        frmt = get_format(query)
        base_filename = file.rsplit(".", 1)[0]
        if args.update or is_newer(file, base_filename + "." + frmt):
            process(query, base_filename, file, args.update)
        else:
            logging.info("Result for '%s' already up to date, use -u to force an update." % file)


def parse_arguments():
    p = ArgumentParser()
    p.add_argument("query_files", nargs="+")
    p.add_argument("-u", "--update", action="store_true", help="Update files even if they are not newer")
    return p.parse_args()


if __name__ == "__main__":
    main(parse_arguments())
    # process("queries/test_query.txt")
    # print_status()
