"""
URL configuration for metaproducts project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
]

# This block is essential for the development server to find and serve
# both user-uploaded media files and your project's static files (like your logo).
if settings.DEBUG:
    # This line serves media files from your MEDIA_ROOT.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # This new line explicitly tells the server how to handle static files
    # from your STATIC_ROOT, which is the most reliable method.
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
