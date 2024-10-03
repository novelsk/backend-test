import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def item(factory):
    return factory.item(bound=False)


@pytest.fixture
def ya_item(factory):
    return factory.item(bound=False)


def test_unbind_one_item_from_another_product(api, item, ya_item):
    item.binder.bind_with_item(ya_item)

    api.post(
        f"/api/v1/inventory/items/{item.id}/unbind_from/{ya_item.id}/",
        expected_status_code=200,
    )

    assert item.r().product is None
    assert ya_item.r().product is not None


def test_unbinder_result(api, item, ya_item):
    item.binder.bind_with_item(ya_item)

    got = api.post(
        f"/api/v1/inventory/items/{item.id}/unbind_from/{ya_item.id}/",
        expected_status_code=200,
    )

    got = got["affected_items"][0]
    assert got["id"] == item.id
    assert got["gmid"] is None


def test_400_on_logic_exceptions(api, item):
    got = api.post(
        f"/api/v1/inventory/items/{item.id}/unbind_from/{item.id}/",
        expected_status_code=400,
    )

    assert "Impossible to unbind from itself" in got[0]


def test_404_on_bad_item(api, item, ya_item):
    api.post(
        f"/api/v1/inventory/items/100500/unbind_from/{ya_item.id}/",
        expected_status_code=404,
    )
    api.post(
        f"/api/v1/inventory/items/{item.id}/unbind_from/100500/",
        expected_status_code=404,
    )
