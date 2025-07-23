from rest_framework import permissions


class IsOwnerOrPublishedOrStaff(permissions.BasePermission):
    """
    Разрешение:
    - Неавторизованным: только опубликованные видео.
    - Авторизованным: опубликованные + собственные видео.
    - Статусным (staff): все видео.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.is_published or obj.owner == request.user

    def has_permission(self, request, view):
        return True  # Объектный уровень используется


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Разрешение:
    - Только владелец видео или staff может редактировать/удалять видео.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner == request.user


class IsAdminUserOnly(permissions.BasePermission):
    """
    Разрешение:
    - Только staff-пользователи могут получить доступ.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
