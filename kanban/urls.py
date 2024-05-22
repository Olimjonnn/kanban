from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kanban.views import (
    GetColumnsView,
    GetSubTasksView,
    BoardsViewSet,
    TasksViewSet,
    MyTokenObtainPairView
)

router = DefaultRouter()
router.register('boards', BoardsViewSet, basename='boards')
router.register('tasks', TasksViewSet, basename='tasks')

urlpatterns = [
    path('get-columns/', GetColumnsView.as_view()),
    path('get-columns/<pk:int>/', GetColumnsView.as_view()),
    path('get-sub-tasks/', GetSubTasksView.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls))
]

