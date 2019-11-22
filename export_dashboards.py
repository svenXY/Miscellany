

import json
import sys
import os
import re
import logging
from pprint import pprint, pformat
from argparse import ArgumentParser
from datadog import initialize, api

logging.basicConfig(level=logging.INFO)

'''Example usage:

Convert dash to json:
python dash_to_json.py get -d 214520 -a your_api_key_here -p your_app_key_here

Convert dash to json, specifying output file:
python dash_to_json.py get -d 214520 -f my_screenboard.json -a your_api_key_here -p your_app_key_here

Create dash from json file:
python dash_to_json.py create -f my_timeboard.json -a your_api_key_here -p your_app_key_here'''

def getAll(filter=None):
    all_boards = api.Dashboard.get_all()['dashboards']
    logging.info(pformat(all_boards))
    if filter:
        return [dash for dash in all_boards if apply_filter(dash['title'], filter)]
    else:
        return all_boards

def apply_filter(title, filters):
    for f in filters:
        logging.info('Filter: %s' % f)
        if re.search(f, title):
            return True
    return False

def print_error(msg):
    print("\nERROR: {}\n".format(msg))
    parser.print_help()
    sys.exit(1)

if __name__ == '__main__':
    parser = ArgumentParser(description='Download dashboards as JSON')
    parser.add_argument('-d', help='The dashboard ID', required=False)
    parser.add_argument('-F', help='Dashobard title filters (regex)', action='append', required=False)
    parser.add_argument('-a', help='Datadog API key', required=False)
    parser.add_argument('-p', help='Datadog APP key', required=False)

    args = parser.parse_args()

    api_key = args.a if args.a else os.environ.get('DD_API_KEY'),
    app_key = args.p if args.p else os.environ.get('DD_APP_KEY'),
    dashboard_id = args.d
    filters = [r"{}".format(f) for f in args.F]

    logging.debug(pformat(filters))

    api_key = api_key[0] if isinstance(api_key, tuple) else api_key
    app_key = app_key[0] if isinstance(app_key, tuple) else app_key

    if not api_key or not app_key:
        print_error("Need to provide api_key and app_key either as an argument or set as an environment variable")
    if not dashboard_id and not filters:
        print_error("Need to provide either a dashboard_id or search filter(s)")

    options = {
        'api_key': api_key,
        'app_key': app_key,
         'api_host': 'https://api.datadoghq.eu',
         'hostname_from_config': False

    }

    initialize(**options)


    if dashboard_id:
        try:
            dashboard = api.Dashboard.get(dashboard_id)
            d = json.loads(dashboard)
            print(d)
        except:
            pass
    if filters:
        try:
            dashboards = getAll(filters)
            for dash in dashboards:
                logging.info(dash.title)
                logging.info(dash.id)
                dashboard = api.Dashboard.get(dash['id'])
                d = json.loads(dashboard)
                print(d)
        except:
            pass

    sys.exit(0)
