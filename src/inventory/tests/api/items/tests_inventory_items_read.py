import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def inventory_item(factory, inventory_owner):
    return factory.item(
        owner=inventory_owner,
    )


@pytest.fixture
def warehouse_item(factory, inventory_item):
    return factory.warehouse_item(item=inventory_item, stock="100.20", price="1005.55")


@pytest.fixture
def listing(factory, inventory_item):
    listing = factory.listing()
    factory.marketplace_item(listing=listing, product=inventory_item.product)

    return listing


@pytest.mark.parametrize(
    "get",
    (
        (lambda api, item: api.get("/api/v1/inventory/items/")["results"][0]),
        (lambda api, item: api.get(f"/api/v1/inventory/items/{item.id}/")),
    ),
)
def test_read_inventory_item(api, inventory_item, get):
    got = get(api, inventory_item)

    assert got["id"] == inventory_item.pk
    assert got["gmid"] == str(inventory_item.product.id)
    assert got["name"] == inventory_item.name
    assert got["unit"] == inventory_item.unit
    assert got["sku"] == inventory_item.sku
    assert got["ean"] == inventory_item.ean


def test_read_owner(api, inventory_item, inventory_owner):
    got = api.get(f"/api/v1/inventory/items/{inventory_item.id}/")

    assert got["owner"]["id"] == inventory_owner.pk
    assert got["owner"]["name"] == inventory_owner.name
    assert got["owner"]["slug"] == inventory_owner.slug


def test_read_warehouse_item(api, inventory_item, warehouse_item):
    got = api.get(f"/api/v1/inventory/items/{inventory_item.id}/")

    got = got["warehouse_items"][0]
    assert got["id"] == warehouse_item.id
    assert got["warehouse_id"] == warehouse_item.warehouse.id
    assert got["stock"] == "100.20"
    assert got["price"] == "1005.55"


def test_total_warehouse_stock_serializing(api, inventory_item, factory):
    factory.warehouse_item(item=inventory_item, stock=300.5)
    factory.warehouse_item(item=inventory_item, stock=500.49)

    got = api.get(f"/api/v1/inventory/items/{inventory_item.id}/")

    assert got["warehouse_total_stock"] == "800.99"


def test_read_empty_warehouse_items(api, inventory_item):
    got = api.get(f"/api/v1/inventory/items/{inventory_item.id}/")

    assert len(got["warehouse_items"]) == 0


def test_zero_total_warehouse_stock_serializing(api, inventory_item):
    got = api.get(f"/api/v1/inventory/items/{inventory_item.id}/")

    assert got["warehouse_total_stock"] == "0.00"


def test_read_listings_item(api, inventory_item, listing):
    got = api.get(f"/api/v1/inventory/items/{inventory_item.id}/")

    got = got["listings"][0]
    assert got["id"] == listing.id
    assert got["name"] == listing.name
    assert got["marketplace_id"] == listing.marketplace.id


def test_read_empty_listings(api, inventory_item):
    got = api.get(f"/api/v1/inventory/items/{inventory_item.id}/")

    assert len(got["listings"]) == 0


@pytest.mark.usefixtures("listing")
def test_read_empty_listings_if_no_product_id(api, inventory_item):
    inventory_item.setattr_and_save("product", None)

    got = api.get(f"/api/v1/inventory/items/{inventory_item.id}/")

    assert len(got["listings"]) == 0


@pytest.mark.usefixtures("listing", "inventory_item")
def test_do_not_read_other_item_listings(api, factory):
    got = api.get(f"/api/v1/inventory/items/{factory.item().id}/")

    assert len(got["listings"]) == 0
