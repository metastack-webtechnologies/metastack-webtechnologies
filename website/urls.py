# website/urls.py (App-level URL configurations)
# THIS IS A NEW FILE! Create it in your website/ directory.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'), # Maps the root of this app to the homepage view
]
