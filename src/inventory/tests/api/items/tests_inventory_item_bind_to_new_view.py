import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def item(factory):
    return factory.item(bound=False)


def test_default_binding(item):
    item.refresh_from_db()

    assert item.product is None


def test_actually_bind_with_new_product(api, item):
    api.post(
        f"/api/v1/inventory/items/{item.id}/bind_with/new/",
        expected_status_code=200,
    )

    item.refresh_from_db()
    assert item.product is not None


def test_binder_result(api, item):
    got = api.post(
        f"/api/v1/inventory/items/{item.id}/bind_with/new/",
        expected_status_code=200,
    )

    got = got["affected_items"][0]
    assert got["id"] == item.id
    assert int(got["gmid"]) >= 10_000_000


def test_400_on_logic_exceptions(api, item):
    item.binder.bind_with_new()

    got = api.post(
        f"/api/v1/inventory/items/{item.id}/bind_with/new/",
        expected_status_code=400,
    )

    assert "Already bind!" in got[0]


def test_404_on_bad_item(api):
    api.post(
        "/api/v1/inventory/items/100500/bind_with/new/",
        expected_status_code=404,
    )
