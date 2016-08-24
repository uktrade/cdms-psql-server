#!/usr/bin/env python

import setuptools
setup_kwargs = {
    'name': 'cdms-psql-server',
    'version': '1.0',
    'description': 'Serve CDMS data from a local PSQL database',
    'author': 'B M Corser',
    'author_email': 'ben@steady.supply',
    'packages': ['cdms_psql_server'],
}

setuptools.setup(**setup_kwargs)
