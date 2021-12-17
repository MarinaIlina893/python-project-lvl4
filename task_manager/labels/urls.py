from django.urls import path
from task_manager.labels import views

urlpatterns = [
    path('create', views.LabelCreate.as_view(), name='label/create'),
    path('', views.LabelListView.as_view(), name='labels'),
    path('<int:pk>/update/', views.LabelUpdate.as_view(), name='label/update'),
    path('<int:pk>/delete/', views.LabelDelete.as_view(), name='label/delete'),
]
