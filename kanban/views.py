from django.shortcuts import render
from rest_framework import viewsets, generics, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from kanban.filters import TasksFilter, BoardsFilter
from kanban.permissions import IsAuthor, IsTaskOwnerOrDeveloper

from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    ListAPIView,
)

from kanban.models import (
    Columns,
    SubTasks,
    Tasks,
    Boards,
    Comment
)

from kanban.serializers import (
    ColumnSerializer,
    SubTaskSerializer,
    TaskSerializer,
    BoardSerializer,
    BoardListSerializer,
    CommentSerializer,
    TaskListSerializsers,
    MyTokenObtainPairSerializer
)


class GetColumnsView(CreateAPIView, ListAPIView, RetrieveAPIView):
    queryset = Columns.objects.all()
    serializer_class = ColumnSerializer
    permission_classes = [AllowAny]


class GetSubTasksView(ListAPIView, RetrieveAPIView):
    queryset = SubTasks.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [AllowAny]


class BoardsViewSet(viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    serializer_class = BoardSerializer
    filterset_class = BoardsFilter
    permission_classes = [IsAuthor]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthor]
        else:
            self.permission_classes = [AllowAny]
        return super(BoardsViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'update',
                           'partial_update', 'destroy'] and self.request.user.is_authenticated:
            return BoardSerializer
        else:
            return BoardListSerializer


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TasksFilter
    permission_classes = [IsAuthenticated, IsTaskOwnerOrDeveloper]

    def get_serializer_class(self):
        if self.action in ['create', 'update',
                           'partial_update', 'destroy'] and self.request.user.is_authenticated:
            return TaskSerializer
        return TaskListSerializsers


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer
