from rest_framework import serializers
from django.utils.text import slugify

from cards.models import Card
from dishes.serializers import DishSerializer

class CardListSerializer(serializers.ModelSerializer):
    """ Base Serializer for card object """

    class Meta:
        model = Card
        fields = ('id', 'name', 'slug', 'description', 'created_at', 'modified_at')
        read_only_fields = ('id', 'slug', 'created_at', 'modified_at')


class CardSerializer(CardListSerializer):
    """ Serializer for card object presented in detail view"""

    dishes = DishSerializer(many=True, write_only=True)

    class Meta(CardListSerializer.Meta):
        fields = CardListSerializer.Meta.fields + ('dishes',)

    
    def create(self, validated_data):
        dishes_data = validated_data.pop('dishes')

        validated_data["slug"] = slugify(validated_data["name"])

        card = Card.objects.create(**validated_data)
    
        for dish_data in dishes_data:
            dish_serializer = DishSerializer(data=dish_data)
    
            if dish_serializer.is_valid(raise_exception=True):
                
                new_dish = dish_serializer.create(dish_serializer.validated_data)
                new_dish.card = card
                new_dish.save()
    
        return card





