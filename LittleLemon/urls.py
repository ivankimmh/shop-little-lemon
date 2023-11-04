from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("LittleLemonDRF.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("myapp/", include("myapp.urls")),
    path("restaurant/", include("restaurant.urls")),
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)  # static 파일을 얹어줘
