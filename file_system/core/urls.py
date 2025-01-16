from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('email-verified-success/', views.email_verified_success, name='email_verified_success'),
    path('login/', views.login_view, name='login'),
    path('ops-dashboard/', views.ops_dashboard, name='ops_dashboard'),
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
    path('upload-file/', views.upload_file, name='upload_file'),
    path('download-file/', views.download_file, name='download_file'),
]
