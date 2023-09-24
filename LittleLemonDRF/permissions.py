from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name="admin").exists())


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.groups.filter(name="manager").exists()
        )


class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.groups.filter(name="delivery_crew").exists()
        )


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.groups.filter(name="customer").exists()
        )
