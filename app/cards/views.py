from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Count
from django.db import transaction

from cards.models import Card
from cards import serializers
from cards.filters import CardFilter


class CardViewSet(viewsets.ModelViewSet):
    """ Manage cards in database """

    filterset_class = CardFilter
    
    def get_queryset(self):
        """ Returns card objects that contains any dishes only for list view
            Returns all card object for other views
        """
        queryset = Card.objects.all()

        if self.action == "list":
            queryset = queryset \
                        .prefetch_related('dishes')\
                        .annotate(dishes_count=Count('dishes__id'))\
                        .filter(dishes__isnull=False)
        
        return queryset


    def get_serializer_class(self):
        """ Returns proper serializer for each action """
        
        if self.action == "list":
            return serializers.CardListSerializer

        else:
            return serializers.CardSerializer


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Custom create view to allow bulk creation of Card objects """
        
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))

        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
