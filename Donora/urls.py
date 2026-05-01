"""Donora URL Configuration"""

from django.contrib import admin
from django.urls import path, include

# Media (serve only in DEBUG)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Main routes from core app
    path('admin-spa/', include('adminspa.urls')),  # Separate admin SPA
]

# Serve uploaded files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

