from django.urls import path
from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.github import views as github_views
urlpatterns = [
    
    # Google login views
    path('google/login/', google_views.oauth2_login, name='google_login'),
    path('google/login/callback/', google_views.oauth2_callback, name='google_callback'),

    # GitHub login views
    path('github/login/', github_views.oauth2_login, name='github_login'),
    path('github/login/callback/', github_views.oauth2_callback, name='github_callback'),
]