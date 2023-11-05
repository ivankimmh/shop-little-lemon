from django.urls import path, include

from rest_framework.routers import DefaultRouter
from LittleLemonDRF import views

router = DefaultRouter()
router.register(r"bookings", views.BookingViewSet)
router.register(r"menu", views.MenuViewSet)

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
] + router.urls
