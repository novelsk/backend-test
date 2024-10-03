from decimal import Decimal

import pytest

from inventory.models import InventoryItem

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def item(factory):
    return factory.item()


@pytest.fixture
def create_warehouse_items(item, factory):
    factory.warehouse_item(item=item, stock=100500.22)
    factory.warehouse_item(item=item, stock=200499.23)


def get_annotated_item(item):
    return InventoryItem.objects.annotate_with_total_stock().get(pk=item.pk)


@pytest.mark.usefixtures("create_warehouse_items")
def test_annotated_with_correct_total_stock(item):
    annotate_item = get_annotated_item(item)

    assert annotate_item.warehouse_total_stock == Decimal("300999.45")


@pytest.mark.usefixtures("create_warehouse_items")
def test_ignore_other_items_in_total_stock_for_item(factory, item):
    factory.warehouse_item(stock=100234)

    annotate_item = get_annotated_item(item)

    assert annotate_item.warehouse_total_stock == Decimal("300999.45")


def test_annotated_total_stock_is_none_if_there_is_no_warehouse_items(item):
    annotate_item = get_annotated_item(item)

    assert annotate_item.warehouse_total_stock == Decimal("0")
