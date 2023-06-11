from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Books API",
        default_version='v1',
        description="Описание проекта",
        terms_of_service="https://www.google.com/policies/terms",
        contact=openapi.Contact(email="admin@company.local"),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("frontend.urls")),
    path("", include("app_profile.urls")),
    path("", include("catalog.urls")),
    path("", include("cart.urls")),
    path("", include("order.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

