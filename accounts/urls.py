from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from accounts import views

# app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignupViewSet.as_view(), name='signup'),
    path('login/', views.LoginViewSet.as_view(), name='login'),
    path('logout/', views.logoutuser, name='logout'),

    path("changepassword/", views.ChangePasswordView.as_view(), name="change-password"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    

    # nav pages
    # path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('rules/', views.rules, name='rules'),

    # other functionality
    # path('api/profile/', views.profile_api, name='profile'),
    # path("profile/", views.user_profile, name="profile"),
    path("profile/", views.ProfileViewSet.as_view(), name="profile"),
    path("health/", views.check_health, name="health"),

    path('verifyemail/', views.verifyemail, name='verifyemail'),
    path('send_otp/', views.verification_otp, name='send_otp'),
    path('forgotpassword/', views.forgotpasswordotp, name='forgotpassword'),
    path('newpassword/', views.newpassword, name='newpassword'),
    path('profileform/', views.profileform, name='profileform'),
    path('', views.home, name='home'),
]
