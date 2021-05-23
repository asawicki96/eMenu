from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.decorators import action, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

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


    def get_serializer_class(self):
        """ Return proper serializer class """

        if self.action == "upload_image":
            return serializers.DishImageSerializer
        
        return self.serializer_class

    @parser_classes((MultiPartParser,))
    @action(detail=True, methods=("POST",), url_path='upload-image')
    def upload_image(self, request, slug=None):
        """ Upload an image to dish """

        dish = self.get_object()
        serializer = self.get_serializer(
            dish,
            data=request.data
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
