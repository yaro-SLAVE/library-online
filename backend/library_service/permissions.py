from rest_framework.permissions import BasePermission


def _get_user_group_names(user):
    return [group.name for group in user.groups.all()]


class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_groups = _get_user_group_names(user)
        return "Librarian" in user_groups


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_groups = _get_user_group_names(user)
        return "Librarian" in user_groups and user.is_superuser


class IsLibrarianOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_groups = _get_user_group_names(user)
        return "Librarian" in user_groups

    def has_object_permission(self, request, view, obj):
        return True
