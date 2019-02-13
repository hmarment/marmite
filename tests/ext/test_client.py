import pytest

from marmite.server.ext.client import Rested, RestedResource


@pytest.fixture(scope='module')
def setup_client():
    """Set up a test client."""
    print('Setting up a test client for external integrations')
    return Rested()


def test_client(setup_client):
    assert isinstance(setup_client, Rested)


def test_client_resources(setup_client):
    assert hasattr(setup_client, 'resources')
    assert isinstance(setup_client.resources, RestedResource)
