from django.urls import path
from CustomerApp import views
urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('Register/', views.Register),
    path('RegAction/', views.RegAction),
    path('LogAction/', views.LogAction),
    path('Home/', views.CustomerHome),
    path('Search/', views.Search),
    path('SearchAction/', views.SearchAction),
    path('BookingConfirm/', views.BookingConfirm),
    path('BookAction/', views.BookAction),
    path('Booked/', views.Booked),
]
