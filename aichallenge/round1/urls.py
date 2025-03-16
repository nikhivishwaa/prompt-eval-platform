from django.urls import path, include
from round1 import views

app_name = 'round1'

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('accounts/', include('accounts.urls')),
    # path('challenege/', include('challenege.urls')),
    path('', views.get_task, name='get_task'),
    path('<int:task_id>', views.submit_task, name='submit_task'),
    path('leaderboard/', views.get_leaderboard, name='get_leaderboard'),
]
