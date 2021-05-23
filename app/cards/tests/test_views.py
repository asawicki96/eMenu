from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from datetime import timedelta

from rest_framework.test import APIClient
from rest_framework import status

from cards.models import Card
from cards.tests.helpers import create_card
from dishes.tests.helpers import create_dish
from dishes.models import Dish

import logging

LIST_CREATE_CARD_URL = reverse('cards:cards-list')

def get_detail_url(slug):
    return reverse('cards:cards-detail', kwargs={"slug": slug})


class PublicCardsAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.example_payload = {
            "name": "Example",
            "description": "Example description"
        }

    def test_create_card_as_anon_user_fails(self):
        """ Test trying to create Card object as non authenticated user ends up with failure """ 

        response = self.client.post(LIST_CREATE_CARD_URL, self.example_payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_retrieve_card_successfull(self):
        """ Test retrieve Card object """

        existing_obj = create_card(**self.example_payload)
        
        response = self.client.get(get_detail_url(existing_obj.slug))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], existing_obj.pk)

    def test_list_view_returns_non_empty_cards(self):
        """ Test if list view return only non empty Card objects """

        empty_card_data = {"name": "Empty", "description": "Empty descr"}
        not_empty_card_data = {"name": "Not Empty", "description": "Not Empty descr"}

        empty_card = create_card(**empty_card_data )
        not_empty_card = create_card(**not_empty_card_data)

        dish_data =  {
            "name": "Example",
            "description": "Example description",
            "price": 1.01,
            "preparation_time": timedelta(seconds=1),
            "card": not_empty_card
        }

        dish = create_dish(**dish_data)

        response = self.client.get(LIST_CREATE_CARD_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    

class PrivateCardsAPITests(TestCase):
    
    def setUp(self):

        self.user = get_user_model().objects.create_user(
            'test@emenu.pl',
            'testpassword'
        )

        self.example_payload = {
            "name": "Example",
            "description": "Example description",
        }

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    

    def test_create_card_as_authenticated_user_successful(self):
        """ Test trying to create card object as authenticated user ends up with success """ 

        response = self.client.post(LIST_CREATE_CARD_URL, self.example_payload)
        
        exists = Card.objects.filter(**response.data).exists()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)


    def test_update_card_successfull(self):
        """ Test update existing Card object """

        existing_obj = create_card(**self.example_payload)

        update_payload = {
            "name": "Changed",
            "description": "Changed description",
        }

        response = self.client.patch(get_detail_url(existing_obj.slug), update_payload)

        updated_obj = Card.objects.get(pk=existing_obj.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_obj.name, update_payload["name"])

    
    def test_create_single_card_without_dishes_successfull(self):
        """ Test create single card without dishes """

        response = self.client.post(LIST_CREATE_CARD_URL, self.example_payload)

        exists = Card.objects.filter(**response.data).exists()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_bulk_create_cards_successful(self):
        """ Test bulk cards create successful """

        payload = [
            {
                "name": "Card1",
                "description": "Card1 Description",
                "dishes": [
                    {
                        "name": "Dish11",
                        "description": "Example description",
                        "price": 1.01,
                        "preparation_time": "00:00:01",
                    },
                    {
                        "name": "Dish12",
                        "description": "Example description",
                        "price": 1.01,
                        "preparation_time": "00:00:01",
                    },
                ]
            },
            {
                "name": "Card2",
                "description": "Card2 Description",
                "dishes": [
                    {
                        "name": "Dish21",
                        "description": "Example description",
                        "price": 1.01,
                        "preparation_time": "00:00:01",
                    },
                    {
                        "name": "Dish22",
                        "description": "Example description",
                        "price": 1.01,
                        "preparation_time": "00:00:01",
                    },
                ]
            }
        ]

        response = self.client.post(LIST_CREATE_CARD_URL, payload, format='json')

        card_names = [card["name"] for card in payload]
        new_cards = Card.objects.filter(name__in=card_names)

        card_1_dishes = Dish.objects.filter(card_id=response.data[0]["id"])
        card_2_dishes = Dish.objects.filter(card_id=response.data[1]["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(new_cards)

        self.assertIsNotNone(card_1_dishes)
        self.assertEqual(len(card_1_dishes), 2)

        self.assertIsNotNone(card_2_dishes)
        self.assertEqual(len(card_2_dishes), 2)





    


