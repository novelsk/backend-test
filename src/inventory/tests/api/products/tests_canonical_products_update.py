import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def product(product):
    product.setattr_and_save("autosync", True)
    return product


def test_update_product(api, product):
    api.put(
        f"/api/v1/inventory/products/{product.id}/",
        {
            "name": "Новое название",
            "ean": "1235",
            "unit": "square.metre",
        },
    )

    product.r()

    assert product.name == "Новое название"
    assert product.ean == "1235"
    assert product.unit == "square.metre"


def test_update_product_result_serializer(api, product):
    got = api.put(
        f"/api/v1/inventory/products/{product.id}/",
        {
            "ean": "12345",
        },
    )

    product.r()

    assert got["id"] == product.id
    assert got["name"] == product.name
    assert got["autosync_item"]["id"] == product.autosync_item.id


def test_autosync_is_off_after_manual_update(api, product):
    api.put(
        f"/api/v1/inventory/products/{product.id}/",
        {
            "ean": "12345",
        },
    )

    assert product.r().autosync is False
