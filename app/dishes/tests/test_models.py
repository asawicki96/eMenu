from django.test import TestCase
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from unittest import mock

from dishes.models import Dish, dish_image_file_path
from dishes.tests.helpers import create_dish
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

recent_timedelta = settings.RECENT_DISH_TIMEDELTA

class DishModelTests(TestCase):

    def setUp(self):

        self.example_data = {
            "name": "Example",
            "description": "Example description",
            "price": 1.01,
            "preparation_time": timedelta(seconds=1)
        }

    
    def test_slug_populated_from_name_on_object_create(self):
        """ Test if slug populates from name on create """

        dish = create_dish(**self.example_data)
        exists = Dish.objects.filter(pk=dish.pk).exists()

        self.assertTrue(exists)
        self.assertEqual(dish.slug, slugify(dish.name))


    def test_dish_get_recent_objs_returns_list_of_recent_update_or_created_objects(self):
        """ Test if Dish.get_recent_objs returns proper value.
            
            recent_dish has modified_at value equal to today - recent_timedelta -> meant to be selected as recent
            not_expected_dish has modified_at value equal to today's date -> meant to not be selected
        """
        
        recent_dish_data = {
            "name": "Recent", 
            "description": "Recent dish description", 
            "price": 1.01, 
            "preparation_time": timedelta(seconds=1)
        }

        not_expected_recent_dish = create_dish(**self.example_data)

        mocked_modified_at = timezone.now() - recent_timedelta

        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked_modified_at)):
            recent_dish = create_dish(**recent_dish_data)
        
        recent_dishes = Dish.get_recent_objs()

        self.assertEqual(len(recent_dishes), 1)
        self.assertIsInstance(recent_dishes, list)
        self.assertEqual(recent_dishes[0].pk, recent_dish.pk)

    @mock.patch('uuid.uuid4')
    def test_dish_filename_uuid(self, mock_uuid):
        """ Test that image is saved in the correct location """

        uuid = 'test_uuid'
        mock_uuid.return_value = uuid

        file_path = dish_image_file_path(None, 'exampleimage.jpg')

        expected_path = f'uploads/dish/{uuid}.jpg'

        self.assertEqual(file_path, expected_path)