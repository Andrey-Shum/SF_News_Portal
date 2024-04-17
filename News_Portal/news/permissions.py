from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение,
    позволяющее редактировать его только аутентифицированным пользователям.
    """

    def has_permission(self, request, view):
        # Разрешения на чтение разрешены для любого запроса,
        # поэтому мы всегда разрешаем запросы GET, HEAD или OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешения на запись
        # разрешены только аутентифицированным пользователям.
        return request.user and request.user.is_authenticated
