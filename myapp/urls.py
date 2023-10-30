from django.urls import path
from . import views

urlpatterns = [
    path("ratings", views.ratings),
    path("", views.form_view, name="home"),
]
