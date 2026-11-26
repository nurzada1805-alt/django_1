from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, NoteStatsAPIView, NoteViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', NoteStatsAPIView.as_view(), name='note-stats'),
]
