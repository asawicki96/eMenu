from dishes.models import Dish
from datetime import timedelta

def create_dish(**params):
    return Dish.objects.create(**params)