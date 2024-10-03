import pytest


@pytest.fixture
def owner(factory):
    return factory.owner()


@pytest.fixture
def ya_owner(factory):
    return factory.owner()
