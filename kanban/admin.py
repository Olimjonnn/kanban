from django.contrib import admin
from kanban.models import (
    Columns,
    SubTasks,
    Tasks,
    Boards,
    Comment
)

admin.site.register(Columns)
admin.site.register(SubTasks)
admin.site.register(Tasks)
admin.site.register(Boards)
admin.site.register(Comment)
