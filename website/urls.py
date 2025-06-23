from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<str:slug>/', views.blog_detail, name='blog_detail'),
    path('team/', views.our_team, name='our_team'),
    path('service/<str:slug>/', views.service_detail, name='service_detail'),
    path('subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'), # NEW URL for newsletter subscription
]
