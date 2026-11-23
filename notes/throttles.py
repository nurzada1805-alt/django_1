from rest_framework.throttling import UserRateThrottle
 
 
class NoteCreateThrottle(UserRateThrottle):
    """Не больше N новых заметок в час на пользователя."""
    scope = 'note_create'
