import pytest
from freezegun import freeze_time

from inventory.models import InventoryItem

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.freeze_time("2032-01-01"),
]


@pytest.fixture(autouse=True)
def settings(settings):
    settings.ITEMS_PER_OWNER_NUMBER = 10

    return settings


@pytest.fixture
def owner_items(owner, factory):
    return factory.cycle(2).item(owner=owner)


@pytest.fixture
def ya_owner_items(ya_owner, factory):
    return factory.cycle(2).item(owner=ya_owner)


def test_grouping_by_owner_works(owner_items, ya_owner_items):
    grouped_items = list(InventoryItem.objects.group_by_owners())

    assert len(grouped_items) == 4

    assert owner_items[0] in grouped_items[:2]
    assert owner_items[1] in grouped_items[:2]

    assert ya_owner_items[0] in grouped_items[2:4]
    assert ya_owner_items[1] in grouped_items[2:4]


def test_grouping_by_owner_limits_items_per_owner(
    settings, owner_items, ya_owner_items
):
    settings.ITEMS_PER_OWNER_NUMBER = 1

    grouped_items = list(InventoryItem.objects.group_by_owners())

    assert len(grouped_items) == 2

    assert grouped_items[0] in owner_items
    assert grouped_items[1] in ya_owner_items


@pytest.mark.usefixtures("owner_items", "ya_owner_items")
def test_grouping_by_owner_for_empty_query_doesnt_break_things():
    grouped_items = list(InventoryItem.objects.none().group_by_owners())

    assert len(grouped_items) == 0


@pytest.mark.parametrize(
    "created, sorting",
    (
        ("2033-01-01", "-created"),
        ("2031-01-01", "created"),
    ),
)
@pytest.mark.usefixtures("owner_items", "ya_owner_items")
def test_grouping_by_owner_respects_initial_ordering_in_each_group(
    settings, factory, owner, ya_owner, created, sorting
):
    settings.ITEMS_PER_OWNER_NUMBER = 1  # Limit to get only top entries for each group
    with freeze_time(created):
        item = factory.item(owner=owner)
        ya_item = factory.item(owner=ya_owner)

    grouped_items = list(InventoryItem.objects.order_by(sorting).group_by_owners())

    assert item == grouped_items[0]
    assert ya_item == grouped_items[1]
