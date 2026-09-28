from django.urls import path
from AdminApp import views
urlpatterns = [
    path('login/', views.login),
    path('logAction/', views.logAction),
    path('Home/', views.Home),
    path('pricedetails/', views.pricedetails),
    path('priceAction/', views.priceAction),
    path('Viewpricedetails/', views.Viewpricedetails,)

]
