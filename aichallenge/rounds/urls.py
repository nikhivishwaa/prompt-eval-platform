from django.urls import path, include
from rounds import views

app_name = 'rounds'

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('accounts/', include('accounts.urls')),
    # path('challenege/', include('challenege.urls')),
    path('round1/', views.get_round1, name='get_task'),
    path('round1/<int:task_id>', views.submit_task, name='submit_task'),
    path('leaderboard/', views.get_leaderboard, name='get_leaderboard'),
]
