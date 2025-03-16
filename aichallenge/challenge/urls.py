from django.urls import path, include
from challenge import views


app_name = 'challenge'

urlpatterns = [
    path('<int:challenge_no>/round1/', include('round1.urls')),
    path('<int:challenge_no>/round2/', include('round2.urls')),
    path('<int:challenge_no>/', views.get_challenge, name='challenge_detail'),
    path('<int:challenge_no>/participate', views.participate, name='participate'),
    path('<int:challenge_no>/leaderboard', views.get_leaderboard, name='leaderboard'),
    
    path('', views.list_challenges, name="all_challenge"),
    # path('', include('round2.urls')),
]