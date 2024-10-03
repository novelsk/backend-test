import pytest
from django.utils import translation
from mixer.backend.django import mixer as _mixer

from app.test.api_client import DRFClient
from app.test.factory import Factory


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def api() -> DRFClient:
    return DRFClient()


@pytest.fixture
def factory() -> Factory:
    return Factory()


@pytest.fixture
def ru():
    with translation.override("ru"):
        yield


@pytest.fixture
def en():
    with translation.override("en"):
        yield
