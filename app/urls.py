from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('sigup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
]