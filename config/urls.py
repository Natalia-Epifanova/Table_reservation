from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/restaurant/")),
    path("restaurant/", include("restaurant.urls", namespace="restaurant")),
    path("users/", include("users.urls", namespace="users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
