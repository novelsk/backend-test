from rest_framework.permissions import BasePermission


class MarketplaceOnly(BasePermission):
    def has_permission(self, request, view):
        if request.marketplace is not None:
            return True

        return False


class StuffAndSuperUserOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.user.is_staff:
            return True

        return False
