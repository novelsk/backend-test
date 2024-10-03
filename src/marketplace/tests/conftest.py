import pytest


@pytest.fixture
def marketplace(factory):
    return factory.marketplace()


@pytest.fixture
def listing(factory, marketplace):
    return factory.listing(marketplace=marketplace)
