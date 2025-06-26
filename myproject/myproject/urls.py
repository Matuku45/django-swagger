"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, re_path, include
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
   

    # Include your app's URLs (e.g., /people/)
    path('', include('myapp.urls')),

    # Swagger/OpenAPI schema JSON/YAML
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Redoc UI (alternative to Swagger UI)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
