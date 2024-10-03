import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def item(factory):
    return factory.item(bound=False)


@pytest.fixture
def ya_item(factory):
    return factory.item(bound=False)


def test_default_binding(item, ya_item):
    item.refresh_from_db()
    ya_item.refresh_from_db()

    assert item.product is None
    assert ya_item.product is None


def test_actually_bind_with_item_product(api, item, ya_item):
    api.post(
        f"/api/v1/inventory/items/{item.id}/bind_with/{ya_item.id}/",
        expected_status_code=200,
    )

    item.refresh_from_db()
    ya_item.refresh_from_db()
    assert item.product is not None
    assert ya_item.product is not None
    assert item.product == item.product


def test_binder_result(api, item, ya_item):
    got = api.post(
        f"/api/v1/inventory/items/{item.id}/bind_with/{ya_item.id}/",
        expected_status_code=200,
    )

    got_1 = got["affected_items"][0]
    got_2 = got["affected_items"][1]
    assert got_1["id"] == item.id
    assert got_2["id"] == ya_item.id
    assert int(got_1["gmid"]) == int(got_2["gmid"])


def test_400_on_logic_exceptions(api, item, ya_item):
    item.binder.bind_with_new()
    ya_item.binder.bind_with_new()

    got = api.post(
        f"/api/v1/inventory/items/{item.id}/bind_with/{ya_item.id}/",
        expected_status_code=400,
    )

    assert "Both products already have bindings!" in got[0]


def test_404_on_bad_item(api, item, ya_item):
    api.post(
        f"/api/v1/inventory/items/100500/bind_with/{ya_item.id}/",
        expected_status_code=404,
    )
    api.post(
        f"/api/v1/inventory/items/{item.id}/bind_with/100500/",
        expected_status_code=404,
    )
