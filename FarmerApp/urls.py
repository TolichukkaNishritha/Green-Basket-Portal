from django.urls import path
from FarmerApp import views
urlpatterns = [
    path('login/', views.login),
    path('Register/', views.Register),
    path('RegAction/', views.RegAction),
    path('LogAction/', views.LogAction),
    path('Home/', views.FarmerHome),
    path('AddProducts/', views.AddProducts),
    path('addPAction/', views.addPAction),
    path('viewproducts/', views.viewproducts),
    path('BookingRequest/', views.BookingRequest),
    path('AssignDeliver/', views.AssignDeliver),


]
