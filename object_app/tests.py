from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json

# Using the standard RequestFactory API to create a form POST request
# Create your tests here.
class GenericObjectAPITests(APITestCase):

    def test_post_data(self):
        data = {'mykey': 'Dorne', 'value': 'House Martell', 'timestamp': '2016-10-26T16:30:30'}
        response = self.client.post('/object/', data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
