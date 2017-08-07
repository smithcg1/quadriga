from __future__ import absolute_import, unicode_literals

import time

import mock
import pytest
import requests

from quadriga import QuadrigaClient
from quadriga import RestClient
from quadriga.exceptions import *
from quadriga.version import VERSION

test_key = 'test_api_key'
test_secret = 'test_api_secret'
test_client_id = 'test_client_id'
test_nonce = 1491481256000
test_book = 'btc_usd'
test_body = {'foo': 'bar'}
test_address = 'test_address'
test_url = 'https://api.quadrigacx.com'
test_headers = {'bar': 'baz'}
test_reason = 'test_reason'


@pytest.fixture(autouse=True)
def patch_time_module(monkeypatch):
    mock_time = mock.MagicMock()
    mock_time.return_value = test_nonce / 1000
    monkeypatch.setattr(time, 'time', mock_time)


@pytest.fixture(autouse=True)
def requests_get(monkeypatch):
    mock_get = mock.MagicMock()
    set_response(mock_get)
    monkeypatch.setattr(requests, 'get', mock_get)
    return mock_get


@pytest.fixture(autouse=True)
def requests_post(monkeypatch):
    mock_post = mock.MagicMock()
    set_response(mock_post)
    monkeypatch.setattr(requests, 'post', mock_post)
    return mock_post


@pytest.fixture(autouse=True)
def logger(monkeypatch):
    mock_logger = mock.MagicMock()
    mock_get_logger = mock.MagicMock()
    mock_get_logger.return_value = mock_logger
    monkeypatch.setattr('logging.getLogger', mock_get_logger)
    return mock_logger


def set_response(http_op, code=200, body=test_body):
    mock_response = mock.MagicMock()
    mock_response.url = test_url
    mock_response.headers = test_headers
    mock_response.status_code = code
    mock_response.json.return_value = body
    mock_response.reason = test_reason
    mock_response.text = body
    http_op.return_value = mock_response
    return mock_response


def build_url(path):
    return RestClient.endpoint_prefix + path


def build_client(default_book=test_book):
    return QuadrigaClient(
        api_key=test_key,
        api_secret=test_secret,
        client_id=test_client_id,
        default_book=default_book
    )


def test_client_init():
    with pytest.raises(InvalidOrderBookError):
        build_client('invalid_book')

    for valid_book in QuadrigaClient.order_books:
        build_client(valid_book)


def test_package_version():
    assert len(VERSION.split('.')) == 3


def test_set_order_book():
    client = build_client(default_book='eth_cad')
    assert getattr(client, '_default_book') == 'eth_cad'

    client.set_default_book('btc_cad')
    assert getattr(client, '_default_book') == 'btc_cad'

    with pytest.raises(InvalidOrderBookError):
        client.set_default_book('invalid_book')


def test_get_summary(requests_get, logger):
    client = build_client()
    output = client.get_summary()
    assert output == test_body
    requests_get.assert_called_with(
        url=build_url('/ticker'),
        params={'book': test_book}
    )
    logger.debug.assert_called_with(
        '[client: test_client_id] get trading summary for btc_usd')
    with pytest.raises(InvalidOrderBookError):
        client.get_summary(book='invalid_book')


def test_request_fail_1(monkeypatch):
    mock_get = mock.MagicMock()
    error_body = {'error': {'code': '123', 'message': 'failed'}}
    set_response(mock_get, code=200, body=error_body)
    monkeypatch.setattr(requests, 'get', mock_get)

    client = build_client()
    with pytest.raises(RequestError) as error:
        client.get_summary()
    assert error.value.url == test_url
    assert error.value.headers == test_headers
    assert error.value.http_code == 200
    assert error.value.error_code == '123'
    assert str(error.value) == '[HTTP 200][ERR 123] failed'


def test_request_fail_2(monkeypatch):
    mock_get = mock.MagicMock()
    set_response(mock_get, code=400)
    monkeypatch.setattr(requests, 'get', mock_get)

    client = build_client()
    with pytest.raises(RequestError) as error:
        client.get_summary()
    assert error.value.url == test_url
    assert error.value.headers == test_headers
    assert error.value.http_code == 400
    assert error.value.error_code is None
    assert str(error.value) == '[HTTP 400] {}'.format(test_reason)


def test_request_fail_3(monkeypatch):
    mock_get = mock.MagicMock()
    mock_response = set_response(mock_get, code=200, body='foo')
    mock_response.json.side_effect = ValueError
    monkeypatch.setattr(requests, 'get', mock_get)

    client = build_client()
    with pytest.raises(RequestError) as error:
        client.get_summary()
    assert error.value.url == test_url
    assert error.value.headers == test_headers
    assert error.value.http_code == 200
    assert error.value.error_code is None
    assert str(error.value) == '[HTTP 200] response body: foo'


def test_get_public_orders(requests_get, logger):
    client = build_client()
    output = client.get_public_orders()
    assert output == test_body
    requests_get.assert_called_with(
        url=build_url('/order_book'),
        params={'book': test_book, 'group': 1}
    )
    logger.debug.assert_called_with(
        '[client: test_client_id] get public orders for btc_usd')

    output = client.get_public_orders(group=False, book='eth_cad')
    assert output == test_body
    requests_get.assert_called_with(
        url=build_url('/order_book'),
        params={'book': 'eth_cad', 'group': 0}
    )
    logger.debug.assert_called_with(
        '[client: test_client_id] get public orders for eth_cad')

    with pytest.raises(InvalidOrderBookError):
        client.get_public_orders(book='invalid_book')


def test_get_public_trades(requests_get, logger):
    client = build_client()
    output = client.get_public_trades()
    assert output == test_body
    requests_get.assert_called_with(
        url=build_url('/transactions'),
        params={'book': test_book, 'time': 'hour'}
    )
    logger.debug.assert_called_with(
        '[client: test_client_id] get recent public trades for btc_usd')

    output = client.get_public_trades(time='minute', book='eth_cad')
    assert output == test_body
    requests_get.assert_called_with(
        url=build_url('/transactions'),
        params={'book': 'eth_cad', 'time': 'minute'}
    )
    logger.debug.assert_called_with(
        '[client: test_client_id] get recent public trades for eth_cad')

    with pytest.raises(InvalidOrderBookError):
        client.get_public_trades(book='invalid_book')


def test_get_orders(requests_post, logger):
    client = build_client()
    output = client.get_orders()
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/open_orders'),
        json={
            'book': test_book,
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] get user's open orders for btc_usd")

    with pytest.raises(InvalidOrderBookError):
        client.get_orders(book='invalid_book')


def test_get_trades(requests_post, logger):
    client = build_client()
    output = client.get_trades()
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/user_transactions'),
        json={
            'book': test_book,
            'limit': 100,
            'offset': 0,
            'sort': 'desc',
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    output = client.get_trades(
        limit=200,
        offset=10,
        sort='asc',
        book='eth_cad'
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] get user's completed trades for eth_cad")

    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/user_transactions'),
        json={
            'book': 'eth_cad',
            'limit': 200,
            'offset': 10,
            'sort': 'asc',
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] get user's completed trades for eth_cad")

    with pytest.raises(InvalidOrderBookError):
        client.get_trades(book='invalid_book')


def test_get_balance(requests_post, logger):
    client = build_client()
    output = client.get_balance()
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/balance'),
        json={
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] get user's account balance")


def test_buy_market_order(requests_post, logger):
    client = build_client()
    output = client.buy_market_order(10)
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/buy'),
        json={
            'book': test_book,
            'amount': 10,
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] buy 10 at market price for btc_usd")

    output = client.buy_market_order(20, 'eth_cad')
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/buy'),
        json={
            'book': 'eth_cad',
            'amount': 20,
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] buy 20 at market price for eth_cad")

    with pytest.raises(InvalidOrderBookError):
        client.buy_market_order(1, 'invalid_book')


def test_buy_limit_order(requests_post, logger):
    client = build_client()
    output = client.buy_limit_order(10, 5)
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/buy'),
        json={
            'book': test_book,
            'amount': 10,
            'price': 5,
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] buy 10 at price of 5 for btc_usd")

    output = client.buy_limit_order(20, 1, 'eth_cad')
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/buy'),
        json={
            'book': 'eth_cad',
            'amount': 20,
            'price': 1,
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] buy 20 at price of 1 for eth_cad")

    with pytest.raises(InvalidOrderBookError):
        client.buy_limit_order(1, 10, 'invalid_book')


def test_sell_market_order(requests_post, logger):
    client = build_client()
    output = client.sell_market_order(10)
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/sell'),
        json={
            'book': test_book,
            'amount': 10,
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] sell 10 at market price for btc_usd")

    output = client.sell_market_order(20, 'eth_cad')
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/sell'),
        json={
            'book': 'eth_cad',
            'amount': 20,
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] sell 20 at market price for eth_cad")

    with pytest.raises(InvalidOrderBookError):
        client.sell_market_order(10, 'invalid_book')


def test_sell_limit_order(requests_post, logger):
    client = build_client()
    output = client.sell_limit_order(10, 5)
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/sell'),
        json={
            'book': test_book,
            'amount': 10,
            'price': 5,
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] sell 10 at price of 5 for btc_usd")

    output = client.sell_limit_order(20, 1, 'eth_cad')
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/sell'),
        json={
            'book': 'eth_cad',
            'amount': 20,
            'price': 1,
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] sell 20 at price of 1 for eth_cad")

    with pytest.raises(InvalidOrderBookError):
        client.sell_limit_order(1, 10, 'invalid_book')


def test_lookup_order(requests_post, logger):
    client = build_client()
    output = client.lookup_order('foobar')
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/lookup_order'),
        json={
            'id': 'foobar',
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] look up order foobar")



def test_cancel_order(requests_post, logger):
    client = build_client()
    output = client.cancel_order('foobar')
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/cancel_order'),
        json={
            'id': 'foobar',
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] cancel order foobar")


def test_get_deposit_address(requests_post, logger):
    client = build_client()
    output = client.get_deposit_address('ether')
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/ether_deposit_address'),
        json={
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] get deposit address for ether")

    output = client.get_deposit_address('bitcoin')
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/bitcoin_deposit_address'),
        json={
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] get deposit address for bitcoin")

    output = client.get_deposit_address('litecoin')
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/litecoin_deposit_address'),
        json={
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] get deposit address for litecoin")

    with pytest.raises(InvalidCurrencyError):
        client.get_deposit_address('invalid_currency')


def test_withdraw(requests_post, logger):
    client = build_client()
    output = client.withdraw('ether', 1000, test_address)
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/ether_withdrawal'),
        json = {
            'address': test_address,
            'amount': 1000,
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] withdraw 1000 ethers to test_address")

    output = client.withdraw('bitcoin', 1000, test_address)
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/bitcoin_withdrawal'),
        json = {
            'address': test_address,
            'amount': 1000,
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] withdraw 1000 bitcoins to test_address")

    output = client.withdraw('litecoin', 1000, test_address)
    assert output == test_body
    requests_post.assert_called_with(
        url=build_url('/litecoin_withdrawal'),
        json = {
            'address': test_address,
            'amount': 1000,
            'key': test_key,
            'nonce': test_nonce,
            'signature': mock.ANY
        }
    )
    logger.debug.assert_called_with(
        "[client: test_client_id] withdraw 1000 litecoins to test_address")

    with pytest.raises(InvalidCurrencyError):
        client.withdraw('invalid_currency', 1000, test_address)
