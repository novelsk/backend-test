import pytest

from inventory.logic.exceptions import ListingEditingException
from marketplace.models import MarketplaceItem

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def item(factory):
    return factory.item()


@pytest.fixture
def marketplace(factory):
    return factory.marketplace()


@pytest.fixture(autouse=True)
def listing(factory, marketplace):
    return factory.listing(marketplace=marketplace)


@pytest.fixture
def ya_listing(factory):
    return factory.listing()


@pytest.fixture
def add_to():
    return lambda item, listing: item.listing_editor.add_to(listing)


@pytest.fixture
def remove_from():
    return lambda item, listing: item.listing_editor.remove_from(listing)


@pytest.fixture
def marketplace_item(marketplace, item):
    return lambda marketplace=marketplace: MarketplaceItem.objects.filter(
        marketplace=marketplace, product=item.product
    ).first()


def test_no_marketplace_items(marketplace_item):
    marketplace_item = marketplace_item()
    assert marketplace_item is None


def test_add_to_listing_creates_marketplace_item(
    add_to, marketplace_item, item, listing
):
    add_to(item, listing)

    marketplace_item = marketplace_item()
    assert marketplace_item is not None


def test_actually_adds_to_listing(add_to, marketplace_item, item, listing):
    add_to(item, listing)

    marketplace_item = marketplace_item()
    assert listing in marketplace_item.listings.all()


def test_add_to_another_listing(ya_listing, add_to, marketplace_item, item, listing):
    add_to(item, listing)
    add_to(item, ya_listing)

    marketplace_item_1 = marketplace_item(marketplace=listing.marketplace)
    assert listing in marketplace_item_1.listings.all()
    assert ya_listing not in marketplace_item_1.listings.all()

    marketplace_item_2 = marketplace_item(marketplace=ya_listing.marketplace)
    assert listing not in marketplace_item_2.listings.all()
    assert ya_listing in marketplace_item_2.listings.all()


def test_raises_if_no_product_on_add(add_to, item, listing):
    item.setattr_and_save("product", None)

    with pytest.raises(ListingEditingException, match=r"product."):
        add_to(item, listing)


def test_raises_if_already_in_listing(add_to, item, listing):
    add_to(item, listing)

    with pytest.raises(ListingEditingException, match=r"Already"):
        add_to(item, listing)


def test_remove_from_listing(add_to, remove_from, marketplace_item, item, listing):
    add_to(item, listing)
    remove_from(item, listing)

    marketplace_item = marketplace_item()
    assert marketplace_item.listings.count() == 0


def test_remove_only_from_current_listing(
    ya_listing, add_to, remove_from, marketplace_item, item, listing
):
    add_to(item, listing)
    add_to(item, ya_listing)

    remove_from(item, listing)

    marketplace_item_1 = marketplace_item(marketplace=listing.marketplace)
    assert marketplace_item_1.listings.count() == 0

    marketplace_item_2 = marketplace_item(marketplace=ya_listing.marketplace)
    assert marketplace_item_2.listings.count() == 1


def test_raises_if_no_product_on_remove(remove_from, item, listing):
    item.setattr_and_save("product", None)

    with pytest.raises(ListingEditingException, match=r"product."):
        remove_from(item, listing)


def test_raises_if_not_in_listing(remove_from, item, listing):
    with pytest.raises(ListingEditingException, match=r"Nothing to remove"):
        remove_from(item, listing)
