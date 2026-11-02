from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Читать может любой, кто прошёл has_permission; менять — только автор."""

    message = 'Изменять заметку может только её автор.'

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS — ('GET', 'HEAD', 'OPTIONS'): они ничего не меняют
        if request.method in SAFE_METHODS:
            return True
        # сравниваем id, а не объекты: так не нужен лишний запрос за автором
        return obj.author_id == request.user.id


class ReadOnly(BasePermission):
    """Пропускает только безопасные методы: GET, HEAD, OPTIONS.

    Нужен для комбинаций вроде [IsAdminUser | ReadOnly]: готового класса
    «только чтение» в DRF нет.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """Доступ к объекту — автору или сотруднику (is_staff).

    В отличие от IsAuthorOrReadOnly, читать чужое тоже нельзя:
    правило одинаково для всех методов.
    """

    message = 'Доступ только автору заметки или администратору.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.author_id == request.user.id