import pytest

from marketplace.models import MarketplaceItem

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def item(factory):
    return factory.item()


@pytest.fixture(autouse=True)
def listing(factory):
    return factory.listing()


@pytest.fixture
def marketplace_item(listing, item):
    return lambda: MarketplaceItem.objects.filter(
        marketplace=listing.marketplace, product=item.product
    ).first()


def test_no_marketplace_items(marketplace_item):
    marketplace_item = marketplace_item()
    assert marketplace_item is None


def test_actually_add_to_listing(api, marketplace_item, item, listing):
    api.post(
        f"/api/v1/inventory/items/{item.id}/add_to_listing/{listing.id}/",
        expected_status_code=200,
    )

    marketplace_item = marketplace_item()
    assert listing in marketplace_item.listings.all()


def test_add_result(api, item, listing):
    got = api.post(
        f"/api/v1/inventory/items/{item.id}/add_to_listing/{listing.id}/",
        expected_status_code=200,
    )

    got = got["affected_items"][0]
    assert got["id"] == item.id


def test_400_on_logic_exceptions(api, item, listing):
    item.listing_editor.add_to(listing)

    got = api.post(
        f"/api/v1/inventory/items/{item.id}/add_to_listing/{listing.id}/",
        expected_status_code=400,
    )

    assert "Already " in got[0]


def test_404(api, item, listing):
    api.post(
        f"/api/v1/inventory/items/100500/add_to_listing/{listing.id}/",
        expected_status_code=404,
    )
    api.post(
        f"/api/v1/inventory/items/{item.id}/add_to_listing/100500/",
        expected_status_code=404,
    )
