# -*- coding: utf-8 -*-
"""
Retrieve data from the presence monitor or set a telephone number.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import json
import sys
import re

try:
    from urllib import request
except ImportError:
    import urllib2 as request

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

if sys.platform.startswith('win'):
    GREEN = '{}'
    RED = '{}'
else:
    GREEN = '\x1b[1m\x1b[32m{}\x1b(B\x1b[m'
    RED = '\x1b[1m\x1b[31m{}\x1b(B\x1b[m'


def print_phone_number(data, pattern):

    TEMPLATE = '{SHORTNAME:<32}{SHORTNUMBER:>12}{MOBIEL:>13}  {PRESENCE:<20}'

    print(' --- Gericht overnemen: *59 / '
          'Prefix interne nummers: 030 2330 --- ')
    print(TEMPLATE.format(SHORTNAME='Naam',
                          SHORTNUMBER='Intern',
                          MOBIEL='Mobiel',
                          PRESENCE='Aanwezig?'))

    print(68 * '-')

    for elem in data:
        if not elem.get('in_office'):
            presence = RED.format('niet')
        elif elem.get('in_drieharingen', False):
            presence = GREEN.format('Driehari')
        elif elem.get('in_vinkenburg', False):
            presence = GREEN.format('Vinkenbu')
        else:
            presence = GREEN.format('Zakkendr')
        elem.update(SHORTNAME=elem['NAAM'][:30])
        elem.update(SHORTNUMBER=elem['number'][:10])
        elem.update(PRESENCE=presence)
        try:
            text = TEMPLATE.format(**elem)
        except KeyError:
            print(elem)
        if re.search(pattern, text, flags=re.IGNORECASE):
            print(text)


def set_telephone(data, pattern, telephone, yes):
    "Set telephone for the first record where the name field matches pattern."
    for elem in data:
        name = elem["NAAM"]
        match = re.search(pattern, name, flags=re.IGNORECASE)
        if match:
            break

    if yes:
        confirmed = True
    elif match:
        confirm_template = "Change the number for {} to {}? [y/N]:\n"
        confirm_message = confirm_template.format(name, telephone)
        try:
            response = raw_input(confirm_message)
        except NameError:
            response = input(confirm_message)

        confirmed = (response == 'y')

    if match and confirmed:
        url = 'http://buildbot.lizardsystem.nl/cgi-bin/set_telephone'
        query_dict = {'id': elem['id'], 'number': telephone}
        query_string = urlencode(query_dict).encode('ascii')
        url_file = request.urlopen(url, query_string)
        response = url_file.read().decode('utf-8')
        if 'is nu %s' % telephone in response:
            print(GREEN.format('Telephone successfully changed.'))
        else:
            print(RED.format('It didn\'t work out. Sorry.'))
    else:
        print('Changing nothing for nobody.')


def naw(pattern, telephone, yes):
    url = 'http://buildbot.lizardsystem.nl/gis/aanwezigheid.json'
    url_file = request.urlopen(url)
    json_str = url_file.read().decode('utf-8')
    url_file.close()

    data = json.loads(json_str)

    if telephone:
        set_telephone(data=data, pattern=pattern,
                      telephone=telephone, yes=yes)
    else:
        print_phone_number(data=data, pattern=pattern)


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pattern',
                        nargs='?',
                        default='',
                        metavar='PATTERN')
    parser.add_argument('-s', '--set-telephone',
                        dest='telephone',
                        help='Change the phone number')
    parser.add_argument('-y', '--assume-yes', dest='yes', action='store_true')
    return parser


def main():
    """ Call naw with args from parser. """
    kwargs = vars(get_parser().parse_args())
    naw(**kwargs)
