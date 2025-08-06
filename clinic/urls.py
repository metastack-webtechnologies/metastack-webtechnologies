from django.urls import path
from . import views

urlpatterns = [
    path('', views.clinic_landing_page, name='clinic_landing'),
    path('guide/', views.clinic_guide_page, name='clinic_guide'),
]