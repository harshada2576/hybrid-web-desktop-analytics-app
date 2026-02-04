"""
URL routing for API endpoints.

All endpoints are prefixed with /api/ by the main urls.py
"""

from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    
    # Data handling endpoints
    path('upload/', views.upload_dataset, name='upload'),
    path('summary/', views.get_summary, name='summary'),
    path('distribution/', views.get_distribution, name='distribution'),
    path('history/', views.get_history, name='history'),
]
