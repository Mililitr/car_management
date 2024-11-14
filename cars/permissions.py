from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользовательский класс разрешений.
    
    Разрешает чтение всем пользователям, но изменение/удаление
    доступно только владельцу объекта.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверка разрешений для конкретного объекта.

        Args:
            request: HTTP запрос
            view: Представление, обрабатывающее запрос
            obj: Объект, к которому выполняется запрос

        Returns:
            bool: True если у пользователя есть права, False если нет
            
        Примечания:
            - GET, HEAD, OPTIONS разрешены всем пользователям
            - PUT, PATCH, DELETE разрешены только владельцу
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user