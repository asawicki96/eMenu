from rest_framework import viewsets, status
from rest_framework import filters

from dishes.models import Dish
from dishes import serializers

# Create your views here.

class DishViewSet(viewsets.ModelViewSet):
    """ Manage dishes in database """

    lookup_field = 'slug'
    queryset = Dish.objects.all()
    serializer_class = serializers.DishSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'modified_at']

