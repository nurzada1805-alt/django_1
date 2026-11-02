# from rest_framework.pagination import PageNumberPagination
 
 
# class NotePagination(PageNumberPagination):
#     page_size = 10                          # по умолчанию
#     page_size_query_param = 'page_size'     # клиент может попросить другой размер...
#     max_page_size = 50                      # ...но не больше этого
#     ordering = '-id'


# from rest_framework.pagination import LimitOffsetPagination
 
 
# class NoteLimitOffsetPagination(LimitOffsetPagination):
#     default_limit = 10
#     max_limit = 50
 
# # GET /api/notes/?limit=3&offset=3
# # {"count": 26, "next": ".../?limit=3&offset=6",
# #  "previous": ".../?limit=3", "results": [...]}



from rest_framework.pagination import CursorPagination
 
 
class NoteCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'           # обязательно!
 
# GET /api/notes/
# {"next": ".../?cursor=cD0yMDI2LTEwLTAy...", "previous": null, "results": [...]}
