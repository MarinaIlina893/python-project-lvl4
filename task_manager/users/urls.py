from django.urls import path
from .views import IndexView
from task_manager.users import views


urlpatterns = [
    path('', IndexView.as_view()),
]
