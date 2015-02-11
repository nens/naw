#!/usr/bin/python

import os
import naw

def main ():
    absfile = naw.__file__.replace('pyc', 'py')
    os.symlink(absfile, '/usr/local/bin/naw')

if __name__ == '__main__':
    main()
