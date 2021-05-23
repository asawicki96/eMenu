from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from rest_framework.test import APIClient
from rest_framework import status

from dishes.models import Dish
from dishes.tests.helpers import create_dish

LIST_CREATE_DISH_URL = reverse('dishes:dishes-list')

def get_detail_url(slug):
    return reverse('dishes:dishes-detail', kwargs={"slug": slug})


class PublicDishesAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.example_payload = {
            "name": "Example",
            "description": "Example description",
            "price": 1.01,
            "preparation_time": "00:00:01",
        }

    def test_create_dish_as_anon_user_fails(self):
        """ Test trying to create Dish object as non authenticated user ends up with failure """ 

        response = self.client.post(LIST_CREATE_DISH_URL, self.example_payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_retrieve_dish_successfull(self):
        """ Test retrieve Dish object """

        existing_obj = create_dish(**self.example_payload)
        
        response = self.client.get(get_detail_url(existing_obj.slug))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], existing_obj.pk)
    

class PrivateDishesAPITests(TestCase):
    
    def setUp(self):

        self.user = get_user_model().objects.create_user(
            'test@emenu.pl',
            'testpassword'
        )

        self.example_payload = {
            "name": "Example",
            "description": "Example description",
            "price": 1.01,
            "preparation_time": "00:00:01",
        }

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    

    def test_create_dish_as_authenticated_user_successful(self):
        """ Test trying to create Dish object as authenticated user ends up with success """ 

        response = self.client.post(LIST_CREATE_DISH_URL, self.example_payload)

        exists = Dish.objects.filter(**response.data).exists()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)


    def test_update_dish_successfull(self):
        """ Test update existing Dish object """

        existing_obj = create_dish(**self.example_payload)

        update_payload = {
            "name": "Changed",
            "description": "Changed description",
            "price": 1.02,
            "preparation_time": "00:00:02",
        }

        response = self.client.patch(get_detail_url(existing_obj.slug), update_payload)

        updated_obj = Dish.objects.get(pk=existing_obj.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_obj.name, update_payload["name"])

    


