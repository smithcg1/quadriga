Error Handling
--------------

All exceptions designed to be raised by the **quadriga** client inherit from the
base exception :class:`quadriga.exceptions.QuadrigaError`. When a request to
QuadrigaCX fails, the client raises :class:`quadriga.exceptions.RequestError`
which lightly wraps the HTTP response returned from the server.

Here is an example showing how an exception can be caught and handled:

.. code-block:: python

    from quadriga import QuadrigaClient, QuadrigaError

    client = QuadrigaClient(
        api_key='api_key',
        api_secret='api_secret',
        client_id='client_id',
        default_book='btc_usd'
    )
    try:
        # This line should fail due to invalid book
        client.get_summary('invalid_book')
    except QuadrigaError as exc:
        print(exc)
        print(exc.url)
        print(exc.body)
        print(exc.headers)
        print(exc.http_code)
        print(exc.error_code)


Exceptions
==========

Below are all exceptions raised by the **quadriga** client.

.. automodule:: quadriga.exceptions
    :members:
