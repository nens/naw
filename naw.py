#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import json
import urllib2
import sys
import re

def main():
    if sys.platform.startswith('win'):
        GREEN = '{}'
        RED = '{}'
    else:
        GREEN = '\x1b[1m\x1b[32m{}\x1b(B\x1b[m'
        RED = '\x1b[1m\x1b[31m{}\x1b(B\x1b[m'

    TEMPLATE = '{SHORTNAME:<32}{SHORTNUMBER:>12}{MOBIEL:>13}  {PRESENCE:<20}'

    jsonfile = urllib2.urlopen(
        'http://buildbot.lizardsystem.nl/gis/aanwezigheid.json',
    )
    data = json.load(jsonfile)
    jsonfile.close()

    try:
        pattern = sys.argv[1]
    except IndexError:
        pattern = ''

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
        elif elem['in_drieharingen']:
            presence = GREEN.format('Driehari')
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

if __name__ == '__main__':
    main()