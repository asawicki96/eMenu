from rest_framework import serializers

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
