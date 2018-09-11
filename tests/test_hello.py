"""Tests"""
from api.hello import HelloWorld


def test_hello_world():
    """Assert"""
    hello_world = HelloWorld()
    assert hello_world.get() == {'hello': 'world'}
