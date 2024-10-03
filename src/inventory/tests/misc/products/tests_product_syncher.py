import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def sync():
    return lambda product: product.syncher.sync()


@pytest.mark.parametrize(
    "field, value", (("name", ""), ("ean", None), ("unit", "unit"))
)
def test_default_fields(product, field, value):
    assert getattr(product.r(), field) == value


@pytest.mark.parametrize(
    "field, value",
    (("name", "I am a vegetable!"), ("ean", "1231231234444"), ("unit", "kg")),
)
def test_synched_fields(product, sync, field, value):
    sync(product)

    assert getattr(product.r(), field) == value


def test_do_not_sync_if_not_allowed_by_flag(product, sync):
    product.setattr_and_save("autosync", False)

    sync(product)

    assert product.r().name == ""


def test_do_not_sync_if_no_items_to_sync_with(factory, sync):
    product = factory.product(name="")

    sync(product)

    assert product.r().name == ""
