import pytest


@pytest.fixture
def item(factory):
    return factory.item(
        name="I am a vegetable!",
        ean="1231231234444",
        unit="kg",
    )


@pytest.fixture
def product(item):
    return item.product
