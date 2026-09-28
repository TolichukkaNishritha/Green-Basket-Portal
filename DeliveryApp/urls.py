from django.urls import path
from DeliveryApp import views
urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('RegAction/', views.RegAction),
    path('LogAction/', views.LogAction),
    path('Home/', views.DeliveryHome),
    path('Dproducts/',views.Dproducts),
    path('UpdateDeliver/', views.UpdateDeliver),

]
