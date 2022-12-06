from rest_framework import permissions


class AuthorOrAdmileElseReadOnly(permissions.BasePermission):
    """Gives an oppurtunity to change data only to:
       author, moderator or superuser."""
    def has_permission(self, request, view):
        """Gives an oppurtunity to 'POST' only to authorized users."""
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        """Gives an oppurtunity to 'PUT', 'PATCH' or 'DELETE' only to:
           author, moderator or superuser."""
        if (request.method in ['PUT', 'PATCH', 'DELETE']
                and not request.user.is_anonymous):
            return (
                    request.user == obj.author
                    or request.user.is_superuser
                    or request.user.is_admin()
            )
        return request.method in permissions.SAFE_METHODS
