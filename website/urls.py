from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.a_propos, name='about'),
    path('solutions/', views.solutions, name='solutions'),
    path('tarifs/', views.tarifs, name='tarifs'),
    path('contact/', views.contact, name='contact'),
]
