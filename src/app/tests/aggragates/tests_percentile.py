import pytest
from django.contrib.auth.models import User

from app.aggregates import Percentile

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture(autouse=True)
def make_instances(mixer):
    data = list(map(str, range(1, 10)))
    for sortable_user_name in data:
        mixer.blend("auth.User", first_name=sortable_user_name)


@pytest.mark.parametrize(
    "fractions, got_names",
    (
        ([0.5], ["5"]),  # Median
        ([0, 1], ["1", "9"]),  # Min and Max
        ([0.41, 0.49, 0.99], ["4", "5", "9"]),  # Different percentiles
    ),
)
def test_percentiles(fractions, got_names):
    agg = User.objects.aggregate(names=Percentile(fractions, "first_name"))

    assert agg["names"] == got_names


def test_percentiles_got_nothing():
    agg = User.objects.filter(first_name="10").aggregate(
        names=Percentile([0, 1], "first_name")
    )

    assert agg["names"] is None


def test_improper_arguments_1():
    with pytest.raises(ValueError):
        User.objects.aggregate(values=Percentile([], "first_name"))


def test_improper_arguments_2():
    with pytest.raises(ValueError):
        User.objects.aggregate(values=Percentile([0.5], ""))
