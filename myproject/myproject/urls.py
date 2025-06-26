"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI schema setup
schema_view = get_schema_view(
    openapi.Info(
        title="My Project API",
        default_version='v1',
        description="API documentation for My Project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Redirect root to Swagger UI
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),

    # Admin interface
    

    # Include your app's URLs (e.g., /people/)
    path('api/', include('myapp.urls')),

    # Swagger schema in JSON or YAML
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # ReDoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve static files (needed for Swagger UI on Render and production)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
