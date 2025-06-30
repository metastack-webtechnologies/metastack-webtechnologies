from django.urls import path
from . import views

# This list defines all the specific pages within your website application.
# It does not include any other urlconfs, which prevents the RecursionError.
urlpatterns = [
    # Main pages
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('team/', views.team, name='team'),

    # Services
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),

    # Portfolio
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),

    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

    # Actions
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
]
