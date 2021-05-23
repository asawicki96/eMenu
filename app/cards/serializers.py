from rest_framework import serializers

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

    dishes = DishSerializer(many=True, write_only=True, required=False)

    class Meta(CardListSerializer.Meta):
        fields = CardListSerializer.Meta.fields + ('dishes',)

    
    def create(self, validated_data):
        dishes_data = []

        if 'dishes' in validated_data:
            dishes_data = validated_data.pop('dishes')

        card = Card.objects.create(**validated_data)
        self._create_dishes(dishes_data, card)
    
        return card


    def _create_dishes(self, dishes_data: list, card: Card):
        
        if not dishes_data:
            return

        if not isinstance(dishes_data, list):
            return

        for dish_data in dishes_data:
            dish_serializer = DishSerializer(data=dish_data)
    
            if dish_serializer.is_valid(raise_exception=True):
                
                new_dish = dish_serializer.create(dish_serializer.validated_data)
                new_dish.card = card
                new_dish.save()


