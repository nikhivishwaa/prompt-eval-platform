from django.urls import path, include
from . import views

# app_name = 'accounts'

urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('login/', views.userauth, name='login'),
    path('logout/', views.logoutuser, name='logout'),

    # nav pages
    # path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('rules/', views.rules, name='rules'),

    # other functionality
    # path('api/profile/', views.profile_api, name='profile'),
    path("profile/", views.user_profile, name="profile"),
    path('verifyemail/', views.verifyemail, name='verifyemail'),
    path('send_otp/', views.verification_otp, name='send_otp'),
    path('forgotpassword/', views.forgotpasswordotp, name='forgotpassword'),
    path('newpassword/', views.newpassword, name='newpassword'),
    path('profileform/', views.profileform, name='profileform'),
    path('', views.home, name='home'),
]
