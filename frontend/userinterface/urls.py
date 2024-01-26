from django.urls import path
from . import views

app_name = "userinterface"
urlpatterns = [
    path("", views.contact, name="index"),
    ]
