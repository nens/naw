# -*- coding: utf-8 -*-

from setuptools import setup

name = 'naw'
version = '0.1'

install_requires = [
    'setuptools',
]

setup(
    name=name,
    version=version,
    url='',
    author='Arjan Verkerk',
    author_email='arjan.verkerk@nelen-schuurmans.com',
    packages=['naw'],
    zip_safe=False,
    install_requires=install_requires,
    entry_points={'console_scripts': [
        'naw = naw.naw:main'
    ]},
)
