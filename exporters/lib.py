import sys
import os
import re
import logging
import json
from argparse import ArgumentParser

logger = logging.getLogger('lib')


def write_to_file(data, outputdir, *name_elements):
    logger.debug('Write to file')
    try:
        os.mkdir(outputdir)
    except FileExistsError:
        pass
    filename = '_'.join([str(e) for e in name_elements]) + '.json'
    filename = get_valid_filename(filename)
    filename = os.path.join(outputdir, filename)
    with open(filename, 'w') as f:
        logger.info('Dump to %s', filename)
        json.dump(data, f, indent=2)

def print_error(msg):
    logger.error(msg)
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

dd_options = {
    'api_key': '',
    'app_key': '',
    'api_host': 'https://api.datadoghq.eu',
    'hostname_from_config': False

}

def initiaize_parser(description=''):
    parser = ArgumentParser(description=description)
    parser.add_argument('-a', help='Datadog API key', default=os.environ.get('DD_API_KEY'))
    parser.add_argument('-p', help='Datadog APP key', default=os.environ.get('DD_APP_KEY'))
    parser.add_argument('-o', help='Outputdir (default "./exported")', default='./exported')
    return parser

def parse_args(parser, dd_options):
    args = parser.parse_args()

    logger.debug('args: %s' % args)

    if not args.a or not args.p:
        print_error("Need to provide api_key and app_key either as an argument or set as an environment variable")

    dd_options['api_key'] = args.a
    dd_options['app_key'] = args.p

    return args

