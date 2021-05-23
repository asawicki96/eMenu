from cards.models import Card

def create_card(**params):
    return Card.objects.create(**params)