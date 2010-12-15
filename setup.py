# -*- coding: utf-8 -*-
# Copyright (c) 2010 Michael Howitz
# See also LICENSE.txt

import os.path
import setuptools

def read(*path_elements):
    return "\n\n" + file(os.path.join(*path_elements)).read()

version = '1.1dev'

setuptools.setup(
    name='Products.SVGrafZ',
    version=version,
    description="SVG graphs for Zope 2",
    long_description=(
        '.. contents::' +
        read('doc', 'README.txt') +
        read('doc', 'INSTALL.txt') +
        read('doc', 'USAGE.txt') +
        read('doc', 'CHANGES.txt')
        ),
    keywords='svg',
    author='Michael Howitz',
    author_email='mh@gocept.com',
    url='http://code.gocept.com',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        ],
    packages=setuptools.find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages = ['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        ],
    extras_require = dict(
        test=[
            'zope.testing',
            ],
        ),
    )
