from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('campaign_details/', views.campaign_details, name='campaign_details'),
    path('faqs/', views.faqs, name='faqs'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('campaigns/', views.campaigns, name='campaigns'),
    path('register-campaign/', views.register_campaign, name='register_campaign'),
    path('campaign/<int:campaign_id>/', views.campaign_details, name='campaign_details'),
]
