import logging
import re
from pprint import pprint, pformat
from datadog import initialize, api
from lib import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('main')


def getAll(filters=None):
    all = api.Dashboard.get_all()['dashboards']
    logger.debug(pformat(all))
    if filters:
        return [item for item in all if apply_filter(item['title'], filters)]
    else:
        return all

def apply_filter(title, filters):
    for f in filters:
        if re.search(f, title):
            return True
    return False

if __name__ == '__main__':
    parser = initiaize_parser('Download dashboards as JSON')
    parser.add_argument('--id', '-i', help='The dashboard ID', required=False)
    parser.add_argument('--filter', '-F',
            help='Dashobard title filters (regex)',
            action='append', required=False)
    args = parse_args(parser, dd_options)

    if not args.id and not args.filter:
        print_error("Need to provide either a dashboard_id or search filter(s)")

    initialize(**dd_options)


    if args.id:
        try:
            logger.info('Get dashboard with ID %s', args.id)
            dashboard = api.Dashboard.get(args.id)
            logger.debug(dashboard)
            write_to_file(dashboard, args.o, 'dashboard', args.id)
        except BaseException as e:
            logger.error('Failed with %s' % e)
    if args.filter:
        try:
            dashboards = getAll(args.filter)
            for dash in dashboards:
                logger.info('Get dashboard %s (%s)' % (dash['title'], dash['id']))
                dashboard = api.Dashboard.get(dash['id'])
                logger.debug(dashboard)
                write_to_file(dashboard, args.o, 'dashboard', dash['title'], dash['id'])
        except BaseException as e:
            logger.error('Failed with %s' % e)
