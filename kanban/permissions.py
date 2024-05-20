from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """
    Custom permission to only give the author the object access
    """

    message = 'You must be author to have permission to perform this action'
    action = ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy']

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['create']:
            return True
        elif request.method in ['update', 'partial_update', 'destroy'] and request.user == obj.author:
            return True
        return False


class IsTaskOwnerOrDeveloper(permissions.BasePermission):
    """
    Custom permission to only give the assignee the object access
    """

    message = 'You must be assignee to have permission to perform this action'
    action = ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy']

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user == obj.developer:
            if self.action == 'partial_update':
                return True
            return False
        if view.action in ['update', 'partial_update', 'destroy']:
            if user == obj.assignee and obj.assignee == obj.board.author:
                return True
            return False
        elif view.action in ['retrieve']:
            return user == obj.assignee or user == obj.board.author
        elif view.action in ['list']:
            return user.is_authenticated
        return True
