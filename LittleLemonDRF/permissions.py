# from rest_framework import permissions
# from rest_framework.request import Request


# class IsManager(permissions.BasePermission):
#     def has_permission(self, request: Request, view):
#         return bool(
#             request.user and request.user.groups.filter(name="manager").exists()
#         )


# class IsDeliveryCrew(permissions.BasePermission):
#     def has_permission(self, request: Request, view):
#         return bool(
#             request.user and request.user.groups.filter(name="delivery_crew").exists()
#         )


# class IsCustomer(permissions.BasePermission):
#     def has_permission(self, request: Request, view):
#         return bool(
#             request.user and request.user.groups.filter(name="customer").exists()
#         )
