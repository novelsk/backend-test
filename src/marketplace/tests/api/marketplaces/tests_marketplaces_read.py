import pytest

pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    "get",
    (
        (lambda api, m: api.get("/api/v1/marketplace/marketplaces/")["results"][0]),
        (lambda api, m: api.get(f"/api/v1/marketplace/marketplaces/{m.slug}/")),
    ),
)
def test_read_marketplace(api, marketplace, get):
    got = get(api, marketplace)

    assert got["id"] == marketplace.pk
    assert got["name"] == marketplace.name
    assert got["slug"] == marketplace.slug


@pytest.mark.parametrize(
    "is_stuff, is_superuser, expected_status_code",
    [[False, False, 403], [True, False, 200], [False, True, 200]],
)
def test_allowed_for_stuff_and_superuser(
    api, is_stuff, is_superuser, expected_status_code
):
    api.user.is_staff = is_stuff
    api.user.is_superuser = is_superuser
    api.user.save()

    api.get(
        "/api/v1/marketplace/marketplaces/", expected_status_code=expected_status_code
    )
