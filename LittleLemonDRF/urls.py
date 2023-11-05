from django.urls import path, include

from rest_framework.routers import DefaultRouter
from LittleLemonDRF import views

router = DefaultRouter()
router.register(r"bookings", views.BookingViewSet)
router.register(r"menu", views.MenuViewSet)
router.register(r"auth", views.SignUpView, basename="auth")

urlpatterns = router.urls
