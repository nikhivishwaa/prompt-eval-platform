from django.urls import path, include
from challenge import views
from rounds import views as v


app_name = 'challenge'

urlpatterns = [
    #  challenge
    path('', views.list_challenges, name="all_challenge"),
    path('<int:challenge_no>/', views.get_challenge_home, name='challenge_detail'),
    path('<int:challenge_no>/participate', views.participate, name='participate'),
    path('<int:challenge_no>/leaderboard', views.get_leaderboard, name='get_leaderboard'), 
    
    # round 1
    path('<int:challenge_no>/round1/', v.get_round1, name='get_task_r1'),
    path('<int:challenge_no>/round1/<int:task_id>/', v.get_round1_task_submission, name='get_task_submission_r1'),
    path('<int:challenge_no>/round1/<int:task_id>/submit', v.submit_round1_task, name='submit_task_r1'),
    path('<int:challenge_no>/round1/submission', v.get_round1_submission, name='get_submission_r1'),
    path('<int:challenge_no>/round1/leaderboard', v.get_round1_leaderboard, name='get_leaderboard_r1'),
    path('<int:challenge_no>/round1/score', v.get_round1_score, name='get_score_r1'),

    # round 2
    path('<int:challenge_no>/round2/', v.get_round2, name='get_task_r2'),
    path('<int:challenge_no>/round2/<int:task_id>/', v.get_round2_task_submission, name='get_task_submission_r2'),
    path('<int:challenge_no>/round2/<int:task_id>/submit', v.submit_round2_task, name='submit_task_r2'),
    path('<int:challenge_no>/round2/submission', v.get_round2_submission, name='get_submission_r2'),
    path('<int:challenge_no>/round2/leaderboard', v.get_round2_leaderboard, name='get_leaderboard_r2'),
    path('<int:challenge_no>/round2/score', v.get_round2_score, name='get_score_r2'),
]