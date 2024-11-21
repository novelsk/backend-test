from decimal import Decimal

import pytest

from marketplace.models import MarketplaceItem

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def item(factory):
    return factory.item()


@pytest.fixture
def marketplace_item(item, factory):
    return factory.marketplace_item(product=item.product)


@pytest.fixture
def create_warehouse_items(item, factory):
    factory.warehouse_item(item=item, stock=200, price=555.55)
    factory.warehouse_item(item=item, stock=400, price=222.22)
    factory.warehouse_item(item=item, stock=500, price=444.44)


def get_annotated_marketplace_item(item):
    return MarketplaceItem.objects.annotate_with_warehouse().get(pk=item.pk)


@pytest.mark.usefixtures("create_warehouse_items")
def test_annotated_with_warehouse_correct(marketplace_item):
    annotated_marketplace_item = get_annotated_marketplace_item(marketplace_item)
    assert annotated_marketplace_item.total_stock == Decimal(1100)
    assert annotated_marketplace_item.min_price == Decimal("222.22")
    assert annotated_marketplace_item.max_price == Decimal("555.55")
