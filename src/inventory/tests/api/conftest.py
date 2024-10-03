import pytest


@pytest.fixture
def inventory_item(factory, inventory_owner):
    return factory.item(owner=inventory_owner)


@pytest.fixture
def inventory_owner(factory):
    return factory.owner()
