.. quadriga documentation master file, created by
   sphinx-quickstart on Thu Mar 30 01:07:06 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the documentation for **quadriga**, a Python client for QuadrigaCX_,
a cryptocurrency exchange platform based in Vancouver, BC, Canada. It wraps the
latest version of the `REST API`_ provided by the exchange and facilitates the
process of trading bitcoins and ethers.

.. _QuadrigaCX: https://www.quadrigacx.com
.. _REST API: https://www.quadrigacx.com/api_info

.. image:: https://travis-ci.org/joowani/quadriga.svg?branch=master
    :target: https://travis-ci.org/joowani/quadriga

.. image:: https://badge.fury.io/py/quadriga.svg
    :target: https://badge.fury.io/py/quadriga
    :alt: Package version

.. image:: https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6-blue.svg
    :target: https://github.com/joowani/quadriga
    :alt: Python Versions

.. image:: https://coveralls.io/repos/github/joowani/quadriga/badge.svg?branch=master
    :target: https://coveralls.io/github/joowani/quadriga?branch=master
    :alt: Test Coverage

.. image:: https://img.shields.io/github/issues/joowani/quadriga.svg
    :target: https://github.com/joowani/quadriga/issues
    :alt: Issues Open

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/joowani/quadriga/master/LICENSE
    :alt: MIT License

|

Requirements
============

- Python 2.7.x, 3.4.x, 3.5.x or 3.6.x
- Recent version of the requests_ library
- QuadrigaCX API secret, API key and client ID

.. _requests: https://github.com/kennethreitz/requests


Installation
============

To install a stable version from PyPi_:

.. code-block:: bash

    ~$ pip install quadriga


To install the latest version directly from GitHub_:

.. code-block:: bash

    ~$ pip install -e git+git@github.com:joowani/quadriga.git@master#egg=quadriga

Note: ``sudo`` may be required depending on the environment.

.. _PyPi: https://pypi.python.org/pypi/quadriga
.. _GitHub: https://github.com/joowani/quadriga


Contents
========

.. toctree::
    :maxdepth: 1

    intro
    api
    errors