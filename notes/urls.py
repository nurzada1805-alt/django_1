# from django.urls import path
 
# from .views import NoteRetrieveUpdateDestroyAPIView,NoteDetailAPIView,NoteListCreateAPIView
# urlpatterns = [
#     path('notes/<int:pk>/', NoteRetrieveUpdateDestroyAPIView.as_view(), name='note-detail'),
#     path('notes/<slug:slug>/', NoteDetailAPIView.as_view(), name='note-detail-title'),
#     path('notes/', NoteListCreateAPIView.as_view(), name='note-list-create'),
   
# ]


# from django.urls import path
# from .views import NoteViewSet
 
# note_list = NoteViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
# })
 
# note_detail = NoteViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     # 'delete': 'destroy',
# })
 
# urlpatterns = [
#     path('notes/', note_list, name='note-list'),
#     path('notes/<int:pk>/', note_detail, name='note-detail'),
#     path('notes/<slug:slug>/', note_detail, name='note-detail-slug')
# ]




# from django.urls import include, path
# from rest_framework.routers import DefaultRouter
# from .views import NoteViewSet,NoteStatsAPIView
 
# router = DefaultRouter()
# router.register(r'notes', NoteViewSet, basename='note')
 
# urlpatterns = [
#     path('', include(router.urls)),
#     path('stats/', NoteStatsAPIView.as_view(), name='note-stats'),   
# ]



from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet,CategoryViewSet
from rest_framework.authtoken.views import obtain_auth_token
from .views import LogoutView


router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'categories', CategoryViewSet, basename='category')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='api-token'),  #  обычный токен
    path('auth/logout/', LogoutView.as_view(),name='api-logout'),
    # path('stats/', NoteStatsAPIView.as_view(), name='note-stats'),   
]




