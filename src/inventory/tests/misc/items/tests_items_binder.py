import pytest

from inventory.logic.exceptions import ItemBindingException

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def item(factory):
    return factory.item(bound=False)


@pytest.fixture
def ya_item(factory):
    return factory.item(bound=False)


@pytest.fixture
def product(factory):
    return factory.product()


@pytest.fixture
def bind_with_item():
    return lambda item, ya_item: item.binder.bind_with_item(ya_item)


@pytest.fixture
def bind_with_new():
    return lambda item: item.binder.bind_with_new()


def test_no_products_by_default(item, ya_item):
    assert item.product is None
    assert ya_item.product is None


def test_bind_with_new_creates_new_product(item, bind_with_new):
    bind_with_new(item)

    assert item.product is not None


def test_bind_with_existing_one_creates_new_product_for_both(
    item, ya_item, bind_with_item
):
    bind_with_item(item, ya_item)

    assert item.product is not None
    assert ya_item.product is not None
    assert item.product == ya_item.product


def test_bind_with_one_linked_product_1(item, ya_item, bind_with_item, product):
    item.setattr_and_save("product", product)

    bind_with_item(item, ya_item)

    assert ya_item.r().product == product


def test_bind_with_one_linked_product_2(item, ya_item, bind_with_item, product):
    ya_item.setattr_and_save("product", product)

    bind_with_item(ya_item, item)

    assert item.r().product == product


def test_new_bindings_are_actually_stored(item, bind_with_new):
    bind_with_new(item)

    assert item.r().product is not None


def test_item_bindings_are_actually_stored(item, ya_item, bind_with_item):
    bind_with_item(item, ya_item)

    assert item.r().product is not None
    assert ya_item.r().product is not None
    assert item.product == ya_item.product


def test_bind_with_new_is_forbidden_if_already_bind(item, bind_with_new):
    bind_with_new(item)

    with pytest.raises(ItemBindingException):
        bind_with_new(item)


def test_bind_is_forbidden_if_both_already_bind(
    item, ya_item, bind_with_item, bind_with_new
):
    bind_with_new(item)
    bind_with_new(ya_item)

    with pytest.raises(ItemBindingException):
        bind_with_item(item, ya_item)


def test_impossible_to_bind_to_itself(item, bind_with_item):
    with pytest.raises(ItemBindingException):
        bind_with_item(item, item)


def test_impossible_to_bind_within_one_owner(item, ya_item, bind_with_item):
    ya_item.setattr_and_save("owner", item.owner)

    with pytest.raises(ItemBindingException):
        bind_with_item(item, ya_item)
