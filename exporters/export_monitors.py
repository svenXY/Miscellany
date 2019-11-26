import json
import sys
import string
import os
import re
import logging
from pprint import pprint, pformat
from argparse import ArgumentParser
from datadog import initialize, api

logging.basicConfig(level=logging.DEBUG)

'''Example usage:

Convert dash to json:
python dash_to_json.py get -d 214520 -a your_api_key_here -p your_app_key_here

Convert dash to json, specifying output file:
python dash_to_json.py get -d 214520 -f my_screenboard.json -a your_api_key_here -p your_app_key_here

Create dash from json file:
python dash_to_json.py create -f my_timeboard.json -a your_api_key_here -p your_app_key_here'''

def getAll(tags=None):
    all_monitors = api.Monitor.get_all(monitor_tags=tags)
    logging.debug(pformat(all_monitors))
    return all_monitors

def write_to_file(title, id, data):
    logging.debug('Write to file')
    try:
        os.mkdir(outputdir)
    except FileExistsError:
        pass
    filename = get_valid_filename(title)
    filename = os.path.join(outputdir, '_'.join(['monitor', filename, str(id), '.json']))
    with open(filename, 'w') as f:
        logging.info('Dump to %s' % filename)
        json.dump(data, f, indent=2)

def print_error(msg):
    logging.error(msg)
    parser.print_help()
    sys.exit(1)

def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

if __name__ == '__main__':
    parser = ArgumentParser(description='Download monitors as JSON')
    parser.add_argument('-t', help='Monitor tags', default=None)
    parser.add_argument('-a', help='Datadog API key', required=False)
    parser.add_argument('-p', help='Datadog APP key', required=False)
    parser.add_argument('-o', help='Outputdir (default "./export")', default='./export')

    args = parser.parse_args()

    api_key = args.a if args.a else os.environ.get('DD_API_KEY'),
    app_key = args.p if args.p else os.environ.get('DD_APP_KEY'),
    tags = args.t
    outputdir = args.o

    logging.debug('Tags: %s' % tags)

    api_key = api_key[0] if isinstance(api_key, tuple) else api_key
    app_key = app_key[0] if isinstance(app_key, tuple) else app_key

    if not api_key or not app_key:
        print_error("Need to provide api_key and app_key either as an argument or set as an environment variable")

    options = {
        'api_key': api_key,
        'app_key': app_key,
        'api_host': 'https://api.datadoghq.eu',
        'hostname_from_config': False

    }

    initialize(**options)


    try:
        monitors = getAll(tags)
        for mon in monitors:
            logging.info('Get monitor %s (%s)' % (mon['name'], mon['id']))
            monitor = api.Monitor.get(mon['id'])
            logging.debug(monitor)
            write_to_file(mon['name'], mon['id'], monitor)
    except BaseException as e:
        logging.error('Failed with %s' % e)

    sys.exit(0)
