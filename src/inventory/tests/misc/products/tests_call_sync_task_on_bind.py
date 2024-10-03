import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def configure(settings):
    settings.PRODUCTS_AUTOSYNC_ENABLED = True


@pytest.fixture
def item(factory):
    return factory.item(bound=False)


@pytest.fixture
def ya_item(factory):
    return factory.item(bound=False)


@pytest.fixture
def sync_mock(mocker):
    return mocker.patch("inventory.logic.syncher.ProductSyncher.sync")


@pytest.fixture
def sync_init(mocker):
    return mocker.patch(
        "inventory.logic.syncher.ProductSyncher.__init__", return_value=None
    )


@pytest.mark.usefixtures("configure")
def test_call_sync_on_bind_with_item(item, ya_item, sync_mock, sync_init):
    item.binder.bind_with_item(ya_item)

    product = item.product

    sync_mock.assert_called()
    sync_init.assert_called_once_with(product)


@pytest.mark.usefixtures("configure")
def test_call_sync_on_bind_to_new(item, sync_mock, sync_init):
    item.binder.bind_with_new()

    product = item.product

    sync_mock.assert_called()
    sync_init.assert_called_once_with(product)


@pytest.mark.usefixtures("configure")
def test_call_sync_on_unbind(item, ya_item, sync_mock, sync_init):
    item.binder.bind_with_item(ya_item)
    product = item.product

    item.unbinder.unbind_from_item(ya_item)

    assert sync_mock.call_count == 2
    assert sync_init.call_count == 2
    assert sync_init.call_args[0][0] == product


def test_do_not_call_if_setting_is_off(item, sync_mock, sync_init):
    item.binder.bind_with_new()

    assert sync_mock.call_count == 0
    assert sync_init.call_count == 0
