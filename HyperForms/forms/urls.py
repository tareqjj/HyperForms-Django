from django.urls import path
from .views import IndexView, registration_view

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("register/", registration_view, name="registration"),
]
