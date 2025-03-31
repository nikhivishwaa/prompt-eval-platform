from django.urls import path, include
from challenge import views
from rounds import views as v


app_name = 'challenge'

urlpatterns = [
    #  challenge
    path('', views.ChallengeViewSet.as_view(), name="all_challenge"),
    path('<int:challenge_no>/', views.ChallengeDetailViewSet.as_view(), name='challenge_detail'),
    path('<int:challenge_no>/participation', views.ParticipationDetailViewSet.as_view(), name='participate'),
    path('<int:challenge_no>/leaderboard', views.LeaderBoardViewSet.as_view(), name='get_leaderboard'), 
    
    # round 1
    path('<int:challenge_no>/round1/', v.Round1ViewSet.as_view(), name='get_task_r1'),
    path('<int:challenge_no>/round1/<int:task_id>/', v.SubmissionViewSet.as_view(), name='get_task_submission_r1'),

    # round 2
    path('<int:challenge_no>/round2/', v.Round2ViewSet.as_view(), name='get_task_r2'),
    path('<int:challenge_no>/round2/<int:task_id>/', v.SubmissionR2ViewSet.as_view(), name='get_task_submission_r2'),

    # evaluate rounds (admin only)
    path('<int:challenge_no>/evaluate/round1', v.Round1EvaluationViewSet.as_view(), name='get_evaluation_r1'),
    path('<int:challenge_no>/evaluate/round2', v.Round2EvaluationViewSet.as_view(), name='get_evaluation_r2'),
    # end rounds
    path('<int:challenge_no>/end/round1', v.Round1EndViewSet.as_view(), name='end_r1'),
    path('<int:challenge_no>/end/round2', v.Round2EndViewSet.as_view(), name='end_r2'),
    # submissions
    path('<int:challenge_no>/submission/round1', v.get_round1_submission, name='get_submission_r1'),
    path('<int:challenge_no>/submission/round2', v.get_round2_submission, name='get_submission_r2'),
    # leaderboard
    path('<int:challenge_no>/leaderboard/round1', v.get_round1_leaderboard, name='get_leaderboard_r1'),
    path('<int:challenge_no>/leaderboard/round2', v.get_round2_leaderboard, name='get_leaderboard_r2'),
    # score
    path('<int:challenge_no>/score/round1', v.get_round1_score, name='get_score_r1'),
    path('<int:challenge_no>/score/round2', v.get_round2_score, name='get_score_r2'),
]