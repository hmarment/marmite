import pytest

from marmite.server.ext.client import Rested, Resources, Resource


@pytest.fixture(scope='module')
def setup_resource():
    """Set up a test resource."""
    print('Setting up a test resource for external integrations')
    return Resource(name='guardian')


@pytest.fixture(scope='module')
def setup_client(setup_resource):
    """Set up a test client."""
    print('Setting up a test client for external integrations')
    return Rested(resources=Resources([setup_resource]))


def test_client(setup_client):
    assert isinstance(setup_client, Rested)


def test_client_resources(setup_client):
    assert hasattr(setup_client, 'resources')
    assert isinstance(setup_client.resources, Resources)


def test_client_add_resource(setup_client, setup_resource):
    setup_client.resources.register(setup_resource)
    assert len(setup_client.resources.list()) == 1
