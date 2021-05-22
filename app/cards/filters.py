import django_filters

from cards import models

class CardFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    created_at = django_filters.DateTimeFilter(field_name="created_at", )
    modified_at = django_filters.DateTimeFilter(field_name="modified_at")

    ordering = django_filters.OrderingFilter(
        fields = (
            ('name', 'name'),
            ('dishes_count', 'dishes_count')
        )
    )

    class Meta:
        model = models.Card
        fields = {
            "created_at": ('lte', 'gte', 'lt', 'gt'),
            "modified_at": ('lte', 'gte', 'lt', 'gt')
        }