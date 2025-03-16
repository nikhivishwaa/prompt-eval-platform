from django.urls import path, include
from round1 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('accounts/', include('accounts.urls')),
    # path('challenege/', include('challenege.urls')),
    path('', views.get_task),
    path('<int:task_id>', views.submit_task),
]
