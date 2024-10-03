import pytest

from marketplace.models import MarketplaceItem

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def item(factory):
    return factory.item()


@pytest.fixture(autouse=True)
def listing(factory, item):
    listing = factory.listing()
    item.listing_editor.add_to(listing)

    return listing


@pytest.fixture
def marketplace_item(listing, item):
    return lambda: MarketplaceItem.objects.filter(
        marketplace=listing.marketplace, product=item.product
    ).first()


def test_has_one_marketplace_item(marketplace_item, listing):
    marketplace_item = marketplace_item()

    assert listing in marketplace_item.listings.all()


def test_actually_removes_from_listing(api, marketplace_item, item, listing):
    api.post(
        f"/api/v1/inventory/items/{item.id}/remove_from_listing/{listing.id}/",
        expected_status_code=200,
    )

    marketplace_item = marketplace_item()
    assert listing not in marketplace_item.listings.all()


def test_remove_result(api, item, listing):
    got = api.post(
        f"/api/v1/inventory/items/{item.id}/remove_from_listing/{listing.id}/",
        expected_status_code=200,
    )

    got = got["affected_items"][0]
    assert got["id"] == item.id


def test_400_on_logic_exceptions(api, item, listing):
    item.listing_editor.remove_from(listing)

    got = api.post(
        f"/api/v1/inventory/items/{item.id}/remove_from_listing/{listing.id}/",
        expected_status_code=400,
    )

    assert "Nothing to remove" in got[0]


def test_404(api, item, listing):
    api.post(
        f"/api/v1/inventory/items/100500/remove_from_listing/{listing.id}/",
        expected_status_code=404,
    )
    api.post(
        f"/api/v1/inventory/items/{item.id}/remove_from_listing/100500/",
        expected_status_code=404,
    )
