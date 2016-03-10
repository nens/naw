# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import json
import sys
import re

try:
    from urllib import request
except ImportError:
    import urllib2 as request


def print_phone_number(pattern, data):
    if sys.platform.startswith('win'):
        GREEN = '{}'
        RED = '{}'
    else:
        GREEN = '\x1b[1m\x1b[32m{}\x1b(B\x1b[m'
        RED = '\x1b[1m\x1b[31m{}\x1b(B\x1b[m'

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


def set_telephone(data, pattern):
    for elem in data:
        name = elem["NAAM"]
        if re.search(pattern, name, flags=re.IGNORECASE):
            number = raw_input("Type the new number for {}: \n".format(
                name)
            )

            confirm = raw_input(
                "Change the number for {} to {}? [y/N]:\n".format(
                    name, number
                ))
            if confirm == 'y':
                change_url = request.urlopen((
                    'http://buildbot.lizardsystem.nl/cgi-bin/'
                    'set_telephone?id={}&number={}'.format(
                        elem['id'],
                        number
                    )))
                print(change_url.read().decode('utf-8'))
                change_url.close()
            else:
                print('Changing nothing for nobody')


def main():
    url_file = request.urlopen(
        'http://buildbot.lizardsystem.nl/gis/aanwezigheid.json',
    )
    json_str = url_file.read().decode('utf-8')
    url_file.close()

    data = json.loads(json_str)

    try:
        pattern = sys.argv[1]
        if pattern == '--set-telephone':
            set_telephone(data, sys.argv[2])
        elif pattern == '--help':
            print('''
USAGE: naw [NAME]

OPTIONS:
--set-telephone NAME -- Changes the phone number
            ''')
        else:
            print_phone_number(pattern, data)
    except IndexError:
        print_phone_number('', data)
