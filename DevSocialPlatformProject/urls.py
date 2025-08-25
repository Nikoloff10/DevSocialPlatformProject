from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from devsearchey.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('accounts/', include('devsearchey.allauth_urls')),
    path('', include('devsearchey.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'devsearchey.views.custom_404_view'
