from django.urls import path
from task_manager.statuses import views

urlpatterns = [
    path('create/', views.StatusCreate.as_view(), name='status/create'),
    path('', views.StatusListView.as_view(), name='status'),
    path('<int:pk>/update/', views.StatusUpdate.as_view(),
         name='status/update'),
    path('<int:pk>/delete/', views.StatusDelete.as_view(),
         name='status/delete'),
]
