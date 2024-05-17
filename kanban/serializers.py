from rest_framework import serializers
from .models import *


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Columns
        fields = ['id', 'column_name', 'order']


class SubTaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = SubTasks
        fields = ['id', 'task', 'subtask_name']


class BoardSerializer(serializers.ModelSerializer):

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

    def create(self, validated_data):
        columns_data = validated_data.pop('columns')
        board_instance = Boards.objects.create(**validated_data)

        for column in columns_data:
            board_instance.columns.add(column)
            board_instance.save()

        return board_instance

    def update(self, instance, validated_data):
        columns_data = validated_data.pop('columns', [])

        instance.board_name = validated_data.get('board_name', instance.board_name)
        instance.board_name = validated_data.get('author', instance.author)

        instance.columns.set(columns_data)
        instance = super().update(instance, validated_data)

        return instance


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True)

    class Meta:
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
            'developer'
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
        subtasks_data = validated_data.pop('subtasks')

        instance.board = validated_data.get('board', instance.board)
        instance.task_title = validated_data.get('task_title', instance.task_title)
        instance.task_description = validated_data.get('task_description', instance.task_description)
        instance.status = validated_data.get('status', instance.status)
        instance.board = validated_data.get('board', instance.board)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.assignee = validated_data.get('assignee', instance.assignee)
        instance.developer = validated_data.get('developer', instance.developer)

        self.update_subtasks(subtasks_data)

        return instance

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




