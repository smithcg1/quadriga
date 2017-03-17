.. quadriga documentation master file, created by
   sphinx-quickstart on Thu Mar 30 01:07:06 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the documentation for **quadriga**, a Python client for QuadrigaCX_
API v2

.. _QuadrigaCX: https://www.quadrigacx.com

Requirements
============

- Python 2.7.x, 3.4.x or 3.5.x
- Recent version of the requests_ library
- API secret, API key and client ID from a QuadrigaCX account

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