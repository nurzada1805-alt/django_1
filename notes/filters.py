from django_filters import rest_framework as filters
from .models import Note

class NoteFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__slug')
    created_after = filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_before = filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
 
    class Meta:
        model = Note
        fields = ['is_done', 'title', 'category', 'created_after', 'created_before']