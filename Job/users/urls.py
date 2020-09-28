from django.urls import path
from .views import *

app_name = 'users'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register')


]
