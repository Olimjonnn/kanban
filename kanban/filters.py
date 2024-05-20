import django_filters
from kanban.models import Boards, Tasks


class BoardsFilter(django_filters.FilterSet):
    class Meta:
        model = Boards
        fields = ['board_name']


class TasksFilter(django_filters.FilterSet):
    class Meta:
        model = Tasks
        fields = ['task_title', 'status']
