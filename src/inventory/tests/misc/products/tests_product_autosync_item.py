import pytest

pytestmark = [pytest.mark.django_db]


def test_autosync_item_is_some_bound_item(product, item):
    assert product.autosync_item == item


def test_no_bound_items_leads_to_empty_autosync(factory):
    product = factory.product()

    assert product.autosync_item is None
