from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(

    name='ini-config-reader',

    version='0.0.3',

    description='A simple config reader based on python Config Parser.',

    long_description=long_description,

    url='https://github.com/teitiago/ini-config-reader',

    author='Tiago Teixeira',
    author_email='teitiago@gmail.com',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

    ],

    keywords='configuration ini reader',

    packages=find_packages(exclude=['tests']),

)
