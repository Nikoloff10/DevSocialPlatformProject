from django.urls import path

from devsearchey.views import home_view, login_view, register_view, logout_view, profile_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
    path('logout', logout_view, name='logout'),
    path('profile', profile_view, name='profile')
]