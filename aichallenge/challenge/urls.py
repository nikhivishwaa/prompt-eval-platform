from django.urls import path, include
from .views import list_challenges, get_challenge

urlpatterns = [
    path('<int:challenge_no>/round1/', include('round1.urls')),
    path('<int:challenge_no>/round2/', include('round2.urls')),
    path('<int:challenge_no>/', get_challenge),
    path('', list_challenges),
    # path('', include('round2.urls')),
]