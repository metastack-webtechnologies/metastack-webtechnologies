
# from django.urls import path, include
# from . import views

# # This list defines all the specific pages within your website application.
# # It does not include any other urlconfs, which prevents the RecursionError.
# urlpatterns = [
#     # Main pages
#     path('', views.homepage, name='homepage'),
#     path('about/', views.about, name='about'),
#     path('contact/', views.contact, name='contact'),
#     path('team/', views.team, name='team'),

#     # Services
#     path('services/', views.services, name='services'),
#     path('services/<slug:slug>/', views.service_detail, name='service_detail'),

#     #Sub-Services
#     path('', views.clinic_landing_page, name='clinic_landing'),
#     path('guide/', views.clinic_guide_page, name='clinic_guide'),

#     # Portfolio
#     path('portfolio/', views.portfolio, name='portfolio'),
#     path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),

#     # Blog
#     path('blog/', views.blog_list, name='blog_list'),
#     path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

#     # Actions
#     path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
# ]

from django.contrib import admin
from django.urls import path, include
# Import views from your main 'website' app
from website import views as website_views

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    # Main Website URLs
    path('', website_views.homepage, name='homepage'),
    path('about/', website_views.about, name='about'),
    path('contact/', website_views.contact, name='contact'),
    path('team/', website_views.team, name='team'),
    path('portfolio/', website_views.portfolio, name='portfolio'),
    path('portfolio/<int:pk>/', website_views.portfolio_detail, name='portfolio_detail'),
    path('blog/', website_views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', website_views.blog_detail, name='blog_detail'),
    path('subscribe/', website_views.subscribe_newsletter, name='subscribe_newsletter'),

    # Services URLs
    path('services/', website_views.services, name='services'),
    path('services/<slug:slug>/', website_views.service_detail, name='service_detail'),

    # Include the URL patterns from the clinic app
    path('services/clinic/', include('clinic.urls')),
]
