import pytest

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("ru"),
]


@pytest.fixture
def marketplace_item(factory, listing):
    item = factory.item()

    return factory.marketplace_item(
        listing=listing,
        product=item.product,
        status="confirmed",
        status_comment="Hello darkness my old friend",
    )


base_url = "/api/v1/marketplace/listings/"


@pytest.mark.parametrize(
    "get",
    (
        (lambda api, l, i: api.get(f"{base_url}{l.id}/items/")["results"][0]),
        (lambda api, l, i: api.get(f"{base_url}{l.id}/items/{i.id}/")),
    ),
)
def test_read_marketplace_item(api, listing, marketplace_item, get):
    got = get(api, listing, marketplace_item)

    assert got["id"] == marketplace_item.pk
    assert got["gmid"] == str(marketplace_item.product.id)
    assert got["status"] == "confirmed"
    assert got["status_comment"] == "Hello darkness my old friend"


def test_read_marketplace_item_only_for_current_listing(
    factory, api, listing, marketplace_item
):
    another_item = factory.marketplace_item()

    got = api.get(f"{base_url}{listing.id}/items/")["results"]

    assert marketplace_item.id in [i["id"] for i in got]
    assert another_item.id not in [i["id"] for i in got]


def test_read_product(api, listing, marketplace_item):
    product = marketplace_item.product

    got = api.get(f"{base_url}{listing.id}/items/{marketplace_item.id}/")

    got = got["product"]
    assert got["id"] == product.pk
    assert got["name"] == product.name
    assert got["ean"] == product.ean
    assert got["unit"] == product.unit
    assert got["autosync"] == product.autosync


@pytest.mark.parametrize(
    "is_stuff, is_superuser, expected_status_code",
    [[False, False, 403], [True, False, 200], [False, True, 200]],
)
def test_allowed_for_stuff_and_superuser(
    api, listing, is_stuff, is_superuser, expected_status_code
):
    api.user.is_staff = is_stuff
    api.user.is_superuser = is_superuser
    api.user.save()

    api.get(f"{base_url}{listing.id}/items/", expected_status_code=expected_status_code)


def test_marketplace_can_not_get_not_own_listing_items(api, marketplace, factory):
    marketplace.setattr_and_save("user", api.user)
    another_listing = factory.listing()

    api.get(f"{base_url}{another_listing.id}/items/", expected_status_code=404)
