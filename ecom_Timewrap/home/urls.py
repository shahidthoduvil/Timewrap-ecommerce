from django.urls import path
from .import views



urlpatterns = [
    # .......................................................user side.......................................................
    path('',views.home,name="home"),

  

]