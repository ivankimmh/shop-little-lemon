from django.urls import path
from . import views

urlpatterns = [
    # User registration and token generation
    path("api/users", views.CreateUserView.as_view(), name="create_user"),
    path("api/users/users/me/", views.CurrentUserView.as_view(), name="current_user"),
    path("token/login/", views.TokenLoginView.as_view(), name="token_login"),
    # Menu-items endpoints
    path("api/menu-items", views.MenuItemListView.as_view(), name="menu_items_list"),
    path(
        "api/menu-items/<int:menu_item_id>/",
        views.SingleMenuItemView.as_view(),
        name="single_menu_item",
    ),
    # User group management
    path(
        "api/groups/manager/users",
        views.ManagerUsersView.as_view(),
        name="manager_users",
    ),
    path(
        "api/groups/manager/users/<int:user_id>/",
        views.SingleManagerUserView.as_view(),
        name="single_manager_user",
    ),
    path(
        "api/groups/delivery-crew/users",
        views.DeliveryCrewUsersView.as_view(),
        name="delivery_crew_users",
    ),
    path(
        "api/groups/delivery-crew/users/<int:user_id>/",
        views.SingleDeliveryCrewUserView.as_view(),
        name="single_delivery_crew_user",
    ),
    # Cart management
    path(
        "api/cart/menu-items", views.CartMenuItemsView.as_view(), name="cart_menu_items"
    ),
    # Order management
    path("api/orders", views.OrdersView.as_view(), name="orders"),
    path(
        "api/orders/<int:order_id>/",
        views.SingleOrderView.as_view(),
        name="single_order",
    ),
]
