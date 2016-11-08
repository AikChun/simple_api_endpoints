from .models import GenericObject
from .serializers import GenericObjectSerializer
from datetime import datetime
from django.http import Http404
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context, loader 
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
import time

# Create your views here.
def index(request):

    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def map_post_data(data):
    result = {}

    for key, value in data.items():
        result['mykey'] = key
        result['value'] = value

    return result

"""
Map Json format {"mykey": "example_key", "value": "example_value", "created_at": "2016-11-08T20:26:30"}
to 
{"example_key": "example_value", "timestamp": "1231351900"}
"""
def map_get_data_to_user(data):
    result                = {}
    
    # set key and value pair first
    result[data["mykey"]] = data["value"]
    
    # convert created_at time into unit timestamp and assign into json object
    result["timestamp"]   = get_unix_timestamp_from_datetime(data["created_at"])

    return result


"""
converts datetime 2016-11-08T20:26:30 to unix timestamp
"""
def get_unix_timestamp_from_datetime(datetime_data):
    datetime_format = '%Y-%m-%dT%H:%M:%SZ'

    datetime_object = datetime.strptime(datetime_data, datetime_format)

    return int(time.mktime(datetime_object.timetuple()))

class GenericObjectList(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    
    def get(self, request, format=None):
        queryset   = GenericObject.objects.all()
        serializer = GenericObjectSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        #request.data['timestamp'] = datetime.utcfromtimestamp(int(request.data['timestamp'])).isoformat()
        if len(request.data) != 1:
            return  HttpResponseBadRequest('<h1>Bad Request</h1>')

        post_data   = request.data
        mapped_data = map_post_data(post_data)


        serializer = GenericObjectSerializer(data=mapped_data)
        if serializer.is_valid():
            serializer.save()
            return Response(map_get_data_to_user(serializer.data), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenericObjectDetail(APIView):
    """
    Retrieve a GenericObject instance.
    """
    renderer_classes = (JSONRenderer, )
    def get(self, request, mykey, format=None):

        timestamp = self.request.query_params.get('timestamp', None)

        obj = self.get_latest_object(mykey, timestamp)

        if not obj:
            return HttpResponseBadRequest('<h1>Bad Request</h1>')

        serializer = GenericObjectSerializer(obj)

        mapped_data = map_get_data_to_user(serializer.data)

        return Response(mapped_data)

    def get_latest_object(self, key, timestamp=None):
        queryset = GenericObject.objects.filter(mykey=key)

        if timestamp is not None:
            timestamp = datetime.utcfromtimestamp(int(timestamp)).isoformat()
            queryset  = queryset.filter(created_at__lte=timestamp)

        queryset = queryset.order_by('-created_at')

        if len(queryset) <= 0:
            return False

        return queryset[0]

