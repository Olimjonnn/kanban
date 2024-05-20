from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import *
# from django.contrib.auth.models import User
from user.models import User
from typing import Dict, Any
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ColumnSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Columns
        fields = ['id', 'column_name']


class SubTaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = SubTasks
        fields = ['id', 'task', 'subtask_name']
        read_only_fields = ['task']


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boards
        fields = [
            'id',
            'board_name',
            'columns',
        ]


class BoardSerializer(serializers.ModelSerializer):
    columns = serializers.PrimaryKeyRelatedField(queryset=Columns.objects.all(), many=True)

    class Meta:
        model = Boards
        fields = [
            'id',
            'board_name',
            'columns',
            'author',
            'created_at',
            'updated_at'
        ]

    # This function for getting M2M field's more details
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        columns = instance.columns
        columns_data = ColumnSerializer(columns, many=True).data

        representation['columns'] = columns_data

        return representation

    def create(self, validated_data):
        columns_data = validated_data.pop('columns')

        board_instance = Boards.objects.create(**validated_data)
        for column in columns_data:
            board_instance.columns.add(column)
            board_instance.save()

        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        columns_data = validated_data.pop('columns', [])

        instance.board_name = validated_data.get('board_name', instance.board_name)
        instance.board_name = validated_data.get('author', instance.author)

        current_columns = instance.columns.all()
        for column in current_columns:
            if str(column.id) not in columns_data and column.column_name not in columns_data:
                instance.columns.remove(column)

        for column_data in columns_data:
            try:
                column_id = int(column_data)
                column = Columns.objects.get(pk=column_id)

            except ValueError:
                column, created = Columns.objects.get_or_create(column_name=column_data)

            instance.columns.add(column)

        instance.save()

        return instance


class TaskListSerializsers(serializers.ModelSerializer):

    class Meta:
        depth = 1
        model = Tasks
        fields = [
            'id',
            'board',
            'task_title',
            'task_description',
            'status',
            'created_at',
            'updated_at',
            'deadline',
            'assignee',
            'developer',
            'subtasks'
        ]


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True)

    class Meta:
        # depth = 1
        model = Tasks
        fields = [
            'id',
            'board',
            'task_title',
            'task_description',
            'status',
            'created_at',
            'updated_at',
            'deadline',
            'assignee',
            'developer',
            'subtasks'
        ]

    def validate(self, attrs):
        board = attrs.get('board')
        status = attrs.get('status')

        if board and status:
            columns = board.columns.all()
            columns_ids = [column.id for column in columns]

            if status.id not in columns_ids:
                raise serializers.ValidationError("Invalid status for the board's columns.")
        return attrs

    def create(self, validated_data):
        status = validated_data.get('status')
        subtasks = validated_data.pop('subtasks')

        if not status:
            board = validated_data.get('board')
            first_column = board.columns.first()
            validated_data['status'] = first_column

        task_instance = Tasks.objects.create(**validated_data)

        for sb in subtasks:
            SubTasks.objects.create(task=task_instance, **sb)

        return task_instance

    def update(self, instance, validated_data):
        board = validated_data.get('board')
        author_board = board.author

        if instance.assignee == author_board:
            subtasks_data = validated_data.pop('subtasks')

            # instance.board = validated_data.get('board', instance.board)
            instance.task_title = validated_data.get('task_title', instance.task_title)
            instance.task_description = validated_data.get('task_description', instance.task_description)
            instance.status = validated_data.get('status', instance.status)
            instance.board = validated_data.get('board', instance.board)
            instance.deadline = validated_data.get('deadline', instance.deadline)
            instance.assignee = validated_data.get('assignee', instance.assignee)
            instance.developer = validated_data.get('developer', instance.developer)

            self.update_subtasks(subtasks_data)
            instance.save()
            return instance
        else:
            return "You do not have permission to this operation"

    def update_subtasks(self, subtasks: list):
        subtasks_items = dict((i.id, i) for i in self.instance.subtasks.all())
        for item in subtasks:
            if 'id' in item:
                subtasks_by_item = subtasks_items.pop(item['id'])
                subtasks_by_item.subtask_name = item['subtask_name']
                subtasks_by_item.save()
            else:
                SubTasks.objects.create(task=self.instance, **item)
        if len(subtasks_items) > 0:
            for item in subtasks_items.values():
                item.delete()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'task',
            'author',
            'content',
            'created_at',
            'updated_at'
        ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone = CharField()
    password = CharField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        phone = attrs.get("phone")
        password = attrs.get("password")
        if not User.objects.filter(phone=phone).exists():
            raise ValidationError({"authorize": "Your not found", "status": 404})
        user = User.objects.get(phone=phone)

        data = super().validate(attrs)
        data["user_phone"] = user.phone
        return data

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user=user)
        token["phone"] = user.phone
        return token
