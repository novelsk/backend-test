from django.apps import apps
from django.conf import settings

from app.celery import celery


@celery.task
def sync_product_fields_with_related_items(product_id: int):
    if not settings.PRODUCTS_AUTOSYNC_ENABLED:
        return

    product = apps.get_model("inventory.Product").objects.get(pk=product_id)
    product.syncher.sync()
