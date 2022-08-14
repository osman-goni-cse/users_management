from django.urls import path
from .views import home, RegisterView, profile

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView, name='users-register'),
    path('profile/', profile, name='users-profile'),
]