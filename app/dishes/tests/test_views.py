from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from datetime import timedelta
import tempfile
import os

from PIL import Image

from rest_framework.test import APIClient
from rest_framework import status

from dishes.models import Dish
from dishes.tests.helpers import create_dish

LIST_CREATE_DISH_URL = reverse('dishes:dishes-list')

def get_detail_url(pk):
    return reverse('dishes:dishes-detail', kwargs={"pk": pk})

def image_upload_url(dish_pk):
    """ Return URL for dish image upload """

    return reverse('dishes:dishes-upload-image', args=[dish_pk])

class PublicDishesAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.example_payload = {
            "name": "Example",
            "description": "Example description",
            "price": 1.01,
            "preparation_time": timedelta(seconds=1),
        }

    def test_create_dish_as_anon_user_fails(self):
        """ Test trying to create Dish object as non authenticated user ends up with failure """ 

        response = self.client.post(LIST_CREATE_DISH_URL, self.example_payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_retrieve_dish_successfull(self):
        """ Test retrieve Dish object """

        existing_obj = create_dish(**self.example_payload)
        
        response = self.client.get(get_detail_url(existing_obj.pk))

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
            "preparation_time": timedelta(seconds=1),
        }

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    

    def test_create_dish_as_authenticated_user_successful(self):
        """ Test trying to create Dish object as authenticated user ends up with success """ 

        response = self.client.post(LIST_CREATE_DISH_URL, self.example_payload)

        exists = Dish.objects.filter(pk=response.data["id"]).exists()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)


    def test_update_dish_successfull(self):
        """ Test update existing Dish object """

        existing_obj = create_dish(**self.example_payload)

        update_payload = {
            "name": "Changed",
            "description": "Changed description",
            "price": 1.02,
            "preparation_time": timedelta(seconds=2),
        }

        response = self.client.patch(get_detail_url(existing_obj.pk), update_payload)

        updated_obj = Dish.objects.get(pk=existing_obj.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_obj.name, update_payload["name"])

    

class DishImageUploadTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('user@emenu.pl', 'testpass')

        self.client.force_authenticate(self.user)

        self.example_data = {
            "name": "Example",
            "description": "Example description",
            "price": 1.01,
            "preparation_time": timedelta(seconds=1),
        }

        self.dish = create_dish(**self.example_data)

    def tearDown(self):
        self.dish.image.delete()

    def test_upload_image_to_dish(self):
        """ Test uploading an image to dish """

        url = image_upload_url(self.dish.pk)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as named_temp_file:
            img = Image.new('RGB', (10, 10))
            img.save(named_temp_file, format='JPEG')

            named_temp_file.seek(0)

            response = self.client.post(url, {'image': named_temp_file}, format='multipart')

        self.dish.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image', response.data)
        self.assertTrue(os.path.exists(self.dish.image.path))


    def test_upload_image_bad_request(self):
        """ Test uploading invalid image """

        url = image_upload_url(self.dish.pk)

        response = self.client.post(url, {'image': 'not image'}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)