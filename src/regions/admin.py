from django.contrib import admin

from .models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "slug",
    ]

    prepopulated_fields = {
        "slug": ["name"],
    }
