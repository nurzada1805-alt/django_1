from django.db.models import Count, F, Q
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import NoteFilter
from .models import Category, Note
from .pagination import NotePagination
from .permissions import IsAuthorOrReadOnly, ReadOnly
from .serializers import CategoryWithCountSerializer, NoteSerializer
from .throttles import NoteCreateThrottle


class NoteViewSet(viewsets.ModelViewSet):
    """Заметки текущего пользователя: CRUD, фильтры, поиск, сортировка."""

    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = NotePagination
    filterset_class = NoteFilter
    search_fields = ['title', 'text', 'category__name']
    ordering_fields = ['created_at', 'title', 'is_done']
    ordering = ['-created_at']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Note.objects.none()
        queryset = Note.objects.select_related('category', 'author')
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(author=self.request.user)

    def get_throttles(self):
        throttles = super().get_throttles()
        if self.action == 'create':
            throttles.append(NoteCreateThrottle())
        return throttles

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.attachment.delete(save=False)
        instance.delete()

    @extend_schema(request=None, responses={204: None})
    @action(detail=True, methods=['delete'], url_path='attachment')
    def delete_attachment(self, request, pk=None):
        note = self.get_object()
        note.attachment.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=None)
    @action(detail=True, methods=['post'])
    def done(self, request, pk=None):
        note = self.get_object()
        serializer = self.get_serializer(note, data={'is_done': True}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        queryset = self.filter_queryset(self.get_queryset()).filter(is_done=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """Категории: читать могут вошедшие, менять — только админ."""

    serializer_class = CategoryWithCountSerializer
    permission_classes = [IsAuthenticated & (IsAdminUser | ReadOnly)]
    pagination_class = None
    search_fields = ['name']
    ordering_fields = ['name', 'notes_count']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Category.objects.none()
        return Category.objects.annotate(
            notes_count=Count('notes', filter=Q(notes__author=self.request.user))
        )


class NoteStatsAPIView(APIView):
    """Статистика по заметкам текущего пользователя."""

    @extend_schema(responses=inline_serializer(
        name='NoteStats',
        fields={
            'total': serializers.IntegerField(),
            'done': serializers.IntegerField(),
            'active': serializers.IntegerField(),
            'by_category': inline_serializer(
                name='CategoryStats',
                many=True,
                fields={
                    'category_name': serializers.CharField(allow_null=True),
                    'total': serializers.IntegerField(),
                    'done': serializers.IntegerField(),
                },
            ),
        },
    ))
    def get(self, request):
        notes = Note.objects.filter(author=request.user)
        stats = notes.aggregate(
            total=Count('id'),
            done=Count('id', filter=Q(is_done=True)),
        )
        stats['active'] = stats['total'] - stats['done']
        stats['by_category'] = list(
            notes.values(category_name=F('category__name'))
            .annotate(total=Count('id'), done=Count('id', filter=Q(is_done=True)))
            .order_by(F('category_name').asc(nulls_last=True))
        )
        return Response(stats)
