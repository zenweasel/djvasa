#!/usr/bin/env python

import os
import sys
from setuptools import setup


def publish():
    os.system('python setup.py sdist upload')

if sys.argv[-1] == 'publish':
    publish()
    sys.exit()

current_version = sys.version_info[:2]
optional_requirements = []
if current_version < (2, 7) or current_version == (3, 1) or (3, 2):
    optional_requirements.append('argparse>=1.2.1')

setup(
    name='saline',
    version='0.0.1',
    description='Initialize a new Vagrant box based upon your project',
    long_description=open('README.rst').read(),
    author='Brent Hoover',
    author_email='brent@hoover.net',
    url='https://github.com/zenweasel/saline',
    license='MIT',
    keywords='terminal django vagrant saltstack cli',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development'
    ),
    packages=['saline', 'djsaline.templates'],
    package_data={'djsaline': ['templates/*.mustache']},
    entry_points={
        'console_scripts': ['saline = djsaline.main:main'],
    },
    install_requires=[
        "Jinja2 >= 2.7.1",
    ] + optional_requirements,
)
