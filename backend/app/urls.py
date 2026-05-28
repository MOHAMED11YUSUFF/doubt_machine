from django.urls import path
from . import views

urlpatterns = [
    path('create_yusuff/', views.create_yusuff, name='create_yusuff'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('create_admin/', views.create_admin, name='create_admin'),
]