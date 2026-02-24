from rest_framework.permissions import BasePermission

class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        user_groups = [x.name for x in user.groups.all()]

        return "Librarian" in user_groups
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        user_groups = [x.name for x in user.groups.all()]

        return "Librarian" in user_groups and user.is_superuser