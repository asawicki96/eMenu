from dishes.models import Dish

def create_dish(**params):
    return Dish.objects.create(**params)