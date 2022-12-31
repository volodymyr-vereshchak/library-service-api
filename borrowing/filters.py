import django_filters

from .models import Borrow

class BorrowFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name="actual_return_date", label="is_active", lookup_expr="isnull", exclude=True)
    
    class Meta:
        model = Borrow
        fields = ["is_active"]


class BorrowFilterAdmin(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name="actual_return_date", label="is_active", lookup_expr="isnull", exclude=True)
    user_id = django_filters.NumberFilter(field_name="user", lookup_expr="exact", label="user_id")
    
    class Meta:
        model = Borrow
        fields = ["is_active", "user_id"]
