Public API
==========

When *public* API calls are the only calls required for a particular use case,
the **api_key**, **api_secret** and **client_id** parameters need not be set
while initializing the :class:`quadriga.QuadrigaClient`:

.. code-block:: python

    # Initialize without the credentials or the client ID
    client = QuadrigaClient(default_book='btc_usd')

    # Public API calls are allowed
    client.get_summary()
    client.get_public_orders()
    client.get_public_trades()

    # Private (user-specific) API calls should fail:
    client.get_balance()
    client.get_orders()
    client.get_trades()
