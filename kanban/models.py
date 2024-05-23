from django.db import models
from django.db.models import CharField

# from django.contrib.auth.models import User
from user.models import User


class Columns(models.Model):
    column_name = models.CharField(max_length=32, verbose_name='name')

    def __str__(self):
        return self.column_name


class SubTasks(models.Model):
    task = models.ForeignKey("kanban.Tasks", on_delete=models.CASCADE, related_name='subtasks')
    subtask_name = models.CharField(max_length=32, verbose_name='name')

    def __str__(self):
        return f'{self.task.id}'

    class Meta:
        verbose_name_plural = 'SubTasks'


class Boards(models.Model):
    board_name = models.CharField(max_length=100, verbose_name='name')
    columns = models.ManyToManyField("kanban.Columns", related_name='boards')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_board')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.board_name


class Tasks(models.Model):
    board = models.ForeignKey("kanban.Boards", on_delete=models.CASCADE, related_name='tasks')
    task_title = models.CharField(max_length=100, verbose_name='title')
    task_description = models.TextField(verbose_name='description')
    status = models.ForeignKey(Columns, on_delete=models.CASCADE, related_name='task', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateField()
    deadline_status = models.BooleanField(default=False)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_assignee')
    developer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_developer')

    def __str__(self):
        return self.task_title


class Comment(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.task.task_title}'




