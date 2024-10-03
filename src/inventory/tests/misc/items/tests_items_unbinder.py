import pytest

from inventory.logic.exceptions import ItemBindingException

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def item(factory):
    return factory.item(bound=False)


@pytest.fixture
def ya_item(factory, item):
    return factory.item(bound=False)


@pytest.fixture
def unbind_items():
    return lambda item, ya_item: item.unbinder.unbind_from_item(ya_item)


def test_unbind(item, ya_item, unbind_items):
    item.binder.bind_with_item(ya_item)

    unbind_items(item, ya_item)

    assert item.product is None
    assert ya_item.product is not None


def test_unbinding_is_actually_stored(item, ya_item, unbind_items):
    item.binder.bind_with_item(ya_item)

    unbind_items(item, ya_item)

    assert item.r().product is None
    assert ya_item.r().product is not None


def test_unbinding_is_forbidden_if_items_have_no_bindings(item, ya_item, unbind_items):
    with pytest.raises(ItemBindingException):
        unbind_items(item, ya_item)


def test_unbinding_is_forbidden_if_items_were_not_bound_together(
    item, ya_item, unbind_items
):
    item.binder.bind_with_new()
    ya_item.binder.bind_with_new()

    with pytest.raises(ItemBindingException):
        unbind_items(item, ya_item)


def test_impossible_to_unbind_from_itself(item, unbind_items):
    with pytest.raises(ItemBindingException):
        unbind_items(item, item)
