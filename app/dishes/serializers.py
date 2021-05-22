from rest_framework import serializers
from django.utils.text import slugify

from .models import Dish

class DishSerializer(serializers.ModelSerializer):
    """ Serializer for dish object """

    class Meta:
        model = Dish
        fields = (
            'id', 
            'name',
            'slug',
            'description',
            'price',
            'preparation_time',
            'is_vege',
            'created_at',
            'modified_at',
            'card_id'
        )

        read_only_fields = ('id', 'slug', 'created_at', 'modified_at')

    def create(self, validated_data):
        """ Custom create method to set slug for each object created """

        validated_data["slug"] = slugify(validated_data["name"])
        return super().create(validated_data)