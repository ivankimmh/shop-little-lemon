from django.urls import path, include

from rest_framework.routers import DefaultRouter
from LittleLemonDRF import views

# from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
router.register(r"bookings", views.BookingViewSet)

urlpatterns = [
    path("menu-items", views.MenuItemsView.as_view()),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    # path("api-token-auth/", obtain_auth_token),
    # path("categories", views.CategoriesView.as_view()),
    # path("menu-items/<int:pk>", views.SingleMenuItemView.as_view()),
    # path("cart/menu-items", views.CartView.as_view()),
    # path("orders", views.OrderView.as_view()),
    # path("orders/<int:pk>", views.SingleOrderView.as_view()),
    # path(
    #     "groups/manager/users",
    #     views.GroupViewSet.as_view(
    #         {"get": "list", "post": "create", "delete": "destroy"}
    #     ),
    # ),
    # path(
    #     "groups/delivery-crew/users",
    #     views.DeliveryCrewViewSet.as_view(
    #         {"get": "list", "post": "create", "delete": "destroy"}
    #     ),
    # ),
] + router.urls
