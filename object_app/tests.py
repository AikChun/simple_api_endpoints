from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .views import GenericObjectList
import json

# Using the standard RequestFactory API to create a form POST request
# Create your tests here.
class GenericObjectAPITests(APITestCase):

    def test_post_data(self):
        
        data     = {'Dorne': 'House Martell'}
        response = self.client.post('/object/', data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_get_data(self):
        response = self.client.get('/object/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_data(self):

        data     = {'Dorne': 'House Martell'}
        response = self.client.post('/object/', data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
    def test_map_post_data(self):
        obj      = GenericObjectList()
        data     = { "Dorne": "House Martell"}
        
        response = obj.map_post_data(data)
        expected = {
            "mykey": "Dorne",
            "value": "House Martell"
        }
        self.assertEqual(expected, response)