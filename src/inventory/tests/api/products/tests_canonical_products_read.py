import pytest

pytestmark = [pytest.mark.django_db]


def test_read_product(api, product):
    got = api.get(f"/api/v1/inventory/products/{product.id}/")

    assert got["id"] == product.pk
    assert got["name"] == product.name
    assert got["ean"] == product.ean
    assert got["unit"] == product.unit
    assert got["autosync"] == product.autosync
    assert got["autosync_item"]["id"] == product.autosync_item.id
    assert got["autosync_item"]["name"] == product.autosync_item.name


def test_read_inventory_items(api, product, item):
    got = api.get(f"/api/v1/inventory/products/{product.id}/")

    assert got["inventory_items"][0]["id"] == item.pk
    assert got["inventory_items"][0]["name"] == item.name
