# from django.shortcuts import render

# from rest_framework.views import APIView
# from django.shortcuts import get_object_or_404
# from rest_framework import status
# from rest_framework.response import Response

# from .models import Category,Note
# from .serializers import CategorySerializer,NoteSerializer


# class NoteListAPIView(APIView):
#     def get(self, request):
#         notes = Note.objects.all()
#         done = request.query_params.get('done')
        
#         if done == 'true':
#             notes = notes.filter(is_done=True)
#         elif done == 'false':
#             notes = notes.filter(is_done=False)

#         serializer = NoteSerializer(notes, many=True)
#         return Response(serializer.data)

 
#     def post(self, request):
#         serializer = NoteSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class NoteDetailAPIView(APIView):
#     """GET    /api/notes/<pk>/ — одна заметка
#        PUT    /api/notes/<pk>/ — заменить целиком
#        PATCH  /api/notes/<pk>/ — изменить частично
#        DELETE /api/notes/<pk>/ — удалить"""
 
#     def get_object(self, pk):
#         return get_object_or_404(Note, pk=pk)
 
#     def get(self, request, pk):
#         note = self.get_object(pk)
#         serializer = NoteSerializer(note)
#         return Response(serializer.data)
 
#     def put(self, request, pk):
#         note = self.get_object(pk)
#         serializer = NoteSerializer(note, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
 
#     def patch(self, request, pk):
#         note = self.get_object(pk)
#         serializer = NoteSerializer(note, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
 
#     def delete(self, request, pk):
#         note = self.get_object(pk)
#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




# from .models import Category, Note
# from .serializers import CategorySerializer, NoteSerializer
# from rest_framework import generics


# class NoteListCreateAPIView(generics.ListCreateAPIView):
#     """GET /api/notes/ — список
#        POST /api/notes/ — создать"""
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer

#     def get_queryset(self):
#         queryset = Note.objects.all()
#         done = self.request.query_params.get('done')

#         if done == 'true':
#             queryset = queryset.filter(is_done=True)
#         elif done == 'false':
#             queryset = queryset.filter(is_done=False)


#         search = self.request.query_params.get('search')
#         if search:
#             queryset = queryset.filter(title__icontains=search)

#         return queryset

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return NoteSerializer

#         return NoteSerializer


# class NoteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """GET / PUT / PATCH / DELETE /api/notes/<slug>/"""
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#     lookup_field = 'slug'


# class NoteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """GET / PUT / PATCH / DELETE /api/notes/<pk>/"""
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer





# from rest_framework import viewsets
 
# from .models import Note
# from .serializers import NoteSerializer
 
 
# class NoteViewSet(viewsets.ModelViewSet):
#     """Полный CRUD для заметок."""
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer

#     def get_queryset(self):
#         queryset = Note.objects.all()
#         done = self.request.query_params.get('done')

#         if done == 'true':
#             queryset = queryset.filter(is_done=True)
#         elif done == 'false':
#             queryset = queryset.filter(is_done=False)

#         search = self.request.query_params.get('search')
#         if search:
#             queryset = queryset.filter(title__icontains=search)

#         return queryset

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

#     def get_serializer_class(self):
#         if self.action == 'create':
#             return NoteSerializer

#         return NoteSerializer






# from rest_framework import viewsets,status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from .models import Note
# from .serializers import NoteSerializer
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated,IsAdminUser,SAFE_METHODS
# from .permissions import IsAuthorOrReadOnly,ReadOnly
# from .models import Category
# from .serializers import CategorySerializer

 
 
# class NoteViewSet(viewsets.ModelViewSet):
#     queryset = Note.objects.select_related('category', 'author')
#     serializer_class = NoteSerializer
#     permission_classes = [IsAuthenticated,IsAuthorOrReadOnly]
    

#     def get_queryset(self):
#         queryset = Note.objects.select_related('category', 'author')
#         if self.request.user.is_staff:
#             return queryset
#         return queryset.filter(author=self.request.user)  
    
    
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


#     def get_permissions(self):
#         if self.action == 'destroy':
#             return [IsAdminUser()]                 # экземпляры, а не классы!
#         return [permission() for permission in self.permission_classes]


#     @action(detail=False, methods=['delete'], permission_classes=[IsAdminUser])
#     def clear_done(self, request):
#         deleted, _ = self.get_queryset().filter(is_done=True, author=request.user).delete()
#         return Response({'deleted': deleted}, status=status.HTTP_200_OK)

      



#     # def get_queryset(self):
#     #     queryset = Note.objects.all()

#     #     done = self.request.query_params.get('done')
#     #     if done == 'true':
#     #         queryset = queryset.filter(is_done=True)
#     #     elif done == 'false':
#     #         queryset = queryset.filter(is_done=False)

#     #     search = self.request.query_params.get('search')
#     #     if search:
#     #         queryset = queryset.filter(title__icontains=search)

#     #     return queryset
 
#     @action(detail=True, methods=['post'])
#     def done(self, request, pk=None):
#         """POST /api/notes/5/done/ — отметить выполненной"""
#         note = self.get_object()
#         note.is_done = True
#         note.save()
#         return Response(self.get_serializer(note).data)

 
#     @action(detail=False, methods=['get'])
#     def active(self, request):
#         """GET /api/notes/active/ — только невыполненные"""
#         notes = self.get_queryset().filter(is_done=False)
#         return Response(self.get_serializer(notes, many=True).data)


#     @action(detail=True, methods=['post'])
#     def toggle(self, request, pk=None):
#         note = self.get_object()
#         note.is_done = not note.is_done
#         note.save()
#         serializer = self.get_serializer(note)
#         return Response(serializer.data, status=status.HTTP_200_OK)

    
#     @action(detail=False, methods=['delete'])
#     def clear_done(self, request):
#         deleted_count, a = Note.objects.filter(is_done=True).delete()
#         return Response(
#             {'deleted': deleted_count},
#             status=status.HTTP_200_OK
#         )


# class NoteStatsAPIView(APIView):
#     def get(self, request):
#         total = Note.objects.count()
#         done_count = Note.objects.filter(is_done=True).count()
#         return Response({
#             'total': total,
#             'done': done_count,
#             'active': total - done_count
#         })


# class CategoryViewSet(viewsets.ModelViewSet):
#     """Категории: читать могут все, менять — только админ."""
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAdminUser | ReadOnly]




from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, viewsets
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
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Логика выхода (например, удаление токена)
        return Response({"detail": "Successfully logged out."})

def health(request):
    return HttpResponse("OK")
 
 
class NoteViewSet(viewsets.ModelViewSet):
    """Заметки текущего пользователя: CRUD, фильтры, поиск, сортировка."""
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = NotePagination
    filterset_class = NoteFilter
    search_fields = ['title', 'text', 'category__name']
    ordering_fields = ['created_at', 'title', 'is_done']
    ordering = ['-created_at']

    @extend_schema(request=None, responses={204: None})
    @action(detail=True, methods=['delete'], url_path='attachment')
    def delete_attachment(self, request, pk=None):
        note = self.get_object()
        note.attachment.delete(save=True)   # файл с диска + пустое поле в базе
        return Response(status=status.HTTP_204_NO_CONTENT)
 
    def perform_destroy(self, instance):
        instance.attachment.delete(save=False)
        instance.delete()

 
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
            .order_by(F('category_name').asc(nulls_last=True))  # «без категории» — в конце
        )
        return Response(stats)
