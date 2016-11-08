from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from .views import GenericObjectList, GenericObjectDetail
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

    def test_map_post_data(self):
        obj      = GenericObjectList()
        data     = { "Dorne": "House Martell"}
        
        response = obj.map_post_data(data)
        expected = {
            "mykey": "Dorne",
            "value": "House Martell"
        }
        self.assertEqual(expected, response)

class GenericObjectDetailAPITests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view    = GenericObjectList.as_view()
        self.obj     = GenericObjectDetail()

    def test_get_data_by_key(self):

        request  = self.factory.get('/object/Winterfell')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)


    def test_map_get_data_to_user(self):
        
        data = {
            "mykey"      : "Dorne",
            "value"      : "House Martell",
            "created_at" : "2016-11-05T20:02:50Z"
        }

        result = self.obj.map_get_data_to_user(data)

        expected = {
            "Dorne"     : "House Martell",
            "timestamp" : 1478376170
        }

        self.assertEqual(expected, result)

    def test_get_unix_timestamp_from_datetime(self):
        data     = "2016-11-05T20:02:50Z"
        result   = self.obj.get_unix_timestamp_from_datetime(data)
        
        expected = 1478376170

        self.assertEqual(expected, result)

