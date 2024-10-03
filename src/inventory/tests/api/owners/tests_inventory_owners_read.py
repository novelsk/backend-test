import pytest

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    "get",
    (
        (lambda api, owner: api.get("/api/v1/inventory/owners/")["results"][0]),
        (lambda api, owner: api.get(f"/api/v1/inventory/owners/{owner.slug}/")),
    ),
)
def test_read_owner(api, inventory_owner, get):
    got = get(api, inventory_owner)

    assert got["id"] == inventory_owner.pk
    assert got["name"] == inventory_owner.name
    assert got["slug"] == inventory_owner.slug


def test_read_owner_warehouses(api, factory, inventory_owner):
    warehouse = factory.warehouse(owner=inventory_owner)

    got = api.get(f"/api/v1/inventory/owners/{inventory_owner.slug}/")

    got = got["warehouses"][0]
    assert got["id"] == warehouse.pk
    assert got["name"] == warehouse.name
