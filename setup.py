#!/usr/bin/env python
# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license. 
# See the NOTICE for more information.

from __future__ import with_statement

from glob import glob
from imp import load_source
import os
import sys

from gunicorn import __version__

CLASSIFIERS = [
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]

MODULES = (
        'gunicorn',
        'gunicorn.app',
        'gunicorn.http',
        'gunicorn.management',
        'gunicorn.management.commands',
        'gunicorn.workers',
    )

SCRIPTS = glob("bin/gunicorn*")

ENTRY_POINTS = """
    [gunicorn.workers]
    sync=gunicorn.workers.sync:SyncWorker
    eventlet=gunicorn.workers.geventlet:EventletWorker
    gevent=gunicorn.workers.ggevent:GeventWorker
    gevent_wsgi=gunicorn.workers.ggevent:GeventWSGIWorker
    gevent_pywsgi=gunicorn.workers.ggevent:GeventPyWSGIWorker
    tornado=gunicorn.workers.gtornado:TornadoWorker

    [paste.server_runner]
    main=gunicorn.app.pasterapp:paste_server"""


def main():
    if "--setuptools" in sys.argv:
        sys.argv.remove("--setuptools")
        from setuptools import setup
        use_setuptools = True
    else:
        from distutils.core import setup
        use_setuptools = False

    gunicorn = load_source("gunicorn", os.path.join("gunicorn",
        "__init__.py"))

    # read long description
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        long_description = f.read()


    PACKAGES = {}
    for name in MODULES:
        PACKAGES[name] = name.replace(".", "/")

    DATA_FILES = [
        ('gunicorn', ["LICENSE", "MANIFEST.in", "NOTICE", "README.rst", 
                        "THANKS",])
        ]

    options = dict(
            name = 'gunicorn',
            version = gunicorn.__version__,
            description = 'WSGI HTTP Server for UNIX',
            long_description = long_description,
            author = 'Benoit Chesneau',
            author_email = 'benoitc@e-engura.com',
            license = 'MIT',
            url = 'http://gunicorn.org',
            classifiers = CLASSIFIERS,
            packages = PACKAGES.keys(),
            package_dir = PACKAGES,
            scripts = SCRIPTS,
            data_files = DATA_FILES,
    )

    # Python 3: run 2to3
    try:
        from distutils.command.build_py import build_py_2to3
        from distutils.command.build_scripts import build_scripts_2to3
    except ImportError:
        pass
    else:
        options['cmdclass'] = {
            'build_py': build_py_2to3,
            'build_scripts': build_scripts_2to3,
        }

    if use_setuptools:
        options['entry_points'] = ENTRY_POINTS
        
    setup(**options)

if __name__ == "__main__":
    main()
