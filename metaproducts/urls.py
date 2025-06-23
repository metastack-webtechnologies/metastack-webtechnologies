from django.contrib import admin
from django.urls import path, include # Make sure include is imported
from django.conf import settings # Import settings
from django.conf.urls.static import static # Import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')), # Include your website app's URLs
    # New URL for newsletter subscription form submission
    path('newsletter-subscribe/', include('website.urls')), # Direct call to website.urls for newsletter_subscribe
]

# Serve media files only during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
