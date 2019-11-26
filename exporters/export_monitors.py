import logging
from pprint import pprint, pformat
from datadog import initialize, api
from lib import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('main')


def getAll(tags=None):
    all_monitors = api.Monitor.get_all(monitor_tags=tags)
    logger.debug(pformat(all_monitors))
    return all_monitors


if __name__ == '__main__':
    parser = initiaize_parser('Download monitors as JSON')
    parser.add_argument('--tags', '-t', help='Monitor tags', default=None)
    args = parse_args(parser, dd_options)

    logger.debug('Tags: %s' % args.tags)

    initialize(**dd_options)


    try:
        monitors = getAll(args.tags)
        for mon in monitors:
            logger.info('Get monitor %s (%s)' % (mon['name'], mon['id']))
            data = api.Monitor.get(mon['id'])
            logger.debug(data)
            write_to_file(data, args.o, 'monitor', mon['name'], mon['id'])
    except BaseException as e:
        logger.error('Failed with %s' % e)

