Logging
-------

By default, :class:`quadriga.QuadrigaClient` logs API call history using the
``quadriga`` logger at ``logging.DEBUG`` level.

Here is an example showing how the logger can be enabled and customized:

.. code-block:: python

    import logging

    from quadriga import QuadrigaClient

    logger = logging.getLogger('quadriga')

    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Attach a custom handler
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Initialize and use the client to see the changes
    client = QuadrigaClient(
        api_key='api_key',
        api_secret='api_secret',
        client_id='77889',
        default_book='btc_usd'
    )
    client.get_summary()
    client.get_balance()
    client.get_public_orders(book='eth_cad')


The logging output for above would look something like this:

.. code-block:: bash

    [2017-04-12 23:55:51,954] [client: 77889] get trading summary for btc_usd
    [2017-04-12 23:55:52,230] [client: 77889] get user's account balance
    [2017-04-12 23:55:53,741] [client: 77889] get public orders for eth_cad

In order to see the full request information, turn on logging for the requests_
library which **quadriga** uses under the hood:

.. _requests: https://github.com/kennethreitz/requests

.. code-block:: python

    import requests
    import logging

    try: # for Python 3
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
