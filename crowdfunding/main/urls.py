from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('campaign_details/', views.campaign_details, name='campaign_details'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('campaigns/', views.campaigns, name='campaigns'),
    path('register_campaign/', views.register_campaign, name='register_campaign'),
    path('campaign/<int:campaign_id>/', views.campaign_details, name='campaign_details'),
    path('campaign/<int:campaign_id>/contribute/', views.contribute, name='contribute'),

]
