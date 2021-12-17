from django.urls import path
from .views import UserCreate, UserListView, UserUpdate, UserDelete

urlpatterns = [
    path('create', UserCreate.as_view(), name='users/create'),
    path('', UserListView.as_view(), name='users'),
    path('<int:pk>/update/', UserUpdate.as_view(), name='users/update'),
    path('<int:pk>/delete/', UserDelete.as_view(), name='users/delete')
]
