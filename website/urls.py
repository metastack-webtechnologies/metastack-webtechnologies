from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'), # Maps the root of this app to the homepage view
    path('about/', views.about_us, name='about'), # URL for the About Us page
    path('contact/', views.contact_page, name='contact'), # URL for the Contact page
    path('portfolio-detail/', views.portfolio_detail, name='portfolio_detail'), # URL for a generic portfolio detail
]
