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




from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .models import Category, Note
from .permissions import IsAuthorOrReadOnly, ReadOnly
from .serializers import CategorySerializer, NoteSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import NoteFilter
from rest_framework import filters
# from .pagination import NotePagination
# from .pagination import NoteLimitOffsetPagination
from .pagination import NoteCursorPagination
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from .models import Note
from .serializers import NoteSerializer
from .permissions import IsAuthorOrReadOnly
 
 
class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]     # иначе регистрация только для вошедших
 
 
class MeView(generics.RetrieveAPIView):
    """Кто я? Удобно проверять, что токен работает."""
    serializer_class = UserSerializer
 
    def get_object(self):
        return self.request.user



class LogoutView(APIView):
    def post(self, request):
        request.auth.delete()          # request.auth — объект Token
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(
        summary="Получить список заметок",
        description="Возвращает пагинированный список заметок. Поддерживает сортировку и фильтрацию."
    ),
    create=extend_schema(
        summary="Создать новую заметку",
        description="Создает новую заметку. Поле авторизованного пользователя (added_by) проставляется автоматически."
    ),
    retrieve=extend_schema(
        summary="Получить заметку по ID",
        description="Возвращает полную информацию по конкретной заметке по ее уникальному идентификатору."
    ),
    partial_update=extend_schema(
        summary="Частично обновить заметку",
        description="Позволяет обновить отдельные поля (например, заголовок или текст) существующей заметки."
    ),
    destroy=extend_schema(
        summary="Удалить заметку",
        description="Удаляет выбранную заметку. Доступно только автору записи."
    ),
)

    
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = NoteFilter
    search_fields = ['title', 'text', 'category__name']
    ordering_fields = ['created_at', 'title', 'is_done']
    ordering = ['-created_at'] 
    # pagination_class = NotePagination 
    # pagination_class = NoteLimitOffsetPagination    
    # pagination_class = NoteCursorPagination         

 
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):     # это построение схемы
            return Note.objects.none()
        queryset = Note.objects.select_related('category', 'author')
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(author=self.request.user)


    def perform_create(self, serializer):
        """Автор — из запроса, а не из присланного JSON."""
        serializer.save(author=self.request.user)

    def get_permissions(self):
        """Удалять может только админ.

        Внимание: этот метод ЗАМЕНЯЕТ список прав, а не дополняет его.
        Здесь нет IsAuthorOrReadOnly — значит админ удалит и чужую заметку,
        хотя отредактировать её не сможет. Нужно запретить и это —
        верни [IsAdminUser(), IsAuthorOrReadOnly()].
        """
        if self.action == 'destroy':
            return [IsAdminUser()]          # экземпляры, а не классы!
        return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=['delete'], permission_classes=[IsAdminUser])
    def clear_done(self, request):
        """DELETE /api/notes/clear_done/ — удалить свои выполненные заметки.

        author=request.user здесь обязателен: для админа get_queryset()
        возвращает заметки ВСЕХ пользователей, и без фильтра одним запросом
        удалялись бы чужие.

        permission_classes у @action срабатывают только если ViewSet
        подключён роутером: права подставляет router, а не сам декоратор.
        """
        deleted, _ = self.get_queryset().filter(
            is_done=True, author=request.user).delete()
        return Response({'deleted': deleted}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'])
    def active(self, request):
        queryset = self.filter_queryset(self.get_queryset()).filter(is_done=False)
        return Response(self.get_serializer(queryset, many=True).data)


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
    """Категории: читать могут все, менять — только админ."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # атрибут класса ЗАМЕНЯЕТ глобальный IsAuthenticated, поэтому читать
    # категории может и аноним. Нужно «читать — только залогиненным»:
    # permission_classes = [IsAuthenticated & (IsAdminUser | ReadOnly)]
    permission_classes = [IsAdminUser | ReadOnly]
    pagination_class = None                  


