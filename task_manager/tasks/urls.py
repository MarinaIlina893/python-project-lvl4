from django.urls import path
from task_manager.tasks import views

urlpatterns = [
    path('create', views.TaskCreate.as_view(), name='task/create'),
    path('', views.TaskListView.as_view(), name='tasks'),
    path('<int:pk>/update/', views.TaskUpdate.as_view(), name='task/update'),
    path('<int:pk>/delete/', views.TaskDelete.as_view(), name='task/delete'),
    path('<int:pk>', views.TaskDetail.as_view(), name='task/detail'),
]
