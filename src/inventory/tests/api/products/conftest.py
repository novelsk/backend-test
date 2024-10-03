import pytest


@pytest.fixture
def item(factory):
    return factory.item()


@pytest.fixture
def product(item):
    item.product.syncher.sync()
    return item.product
