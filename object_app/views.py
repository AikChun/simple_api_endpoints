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
        mapped_data = self.map_post_data(post_data)


        serializer = GenericObjectSerializer(data=mapped_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Maps json format of {"example_key": "example_value"} to {"mykey": "example_key", "value": "example_value"}
    """
    def map_post_data(self, data):
        result = {}

        for key, value in data.items():
            result['mykey'] = key
            result['value'] = value

        return result

class GenericObjectDetail(APIView):
    """
    Retrieve a GenericObject instance.
    """
    renderer_classes = (JSONRenderer, )
    def get(self, request, mykey, format=None):
        queryset  = GenericObject.objects.filter(mykey=mykey)
        timestamp = self.request.query_params.get('timestamp', None)

        if timestamp is not None:
            timestamp = datetime.utcfromtimestamp(int(timestamp)).isoformat()
            queryset  = queryset.filter(created_at__lte=timestamp)

        if not queryset.count():
            raise Http404

        queryset   = queryset.order_by('-created_at')[0]

        serializer = GenericObjectSerializer(queryset)

        print(serializer.data)

        mapped_data = self.map_get_data_to_user(serializer.data)

        return Response(mapped_data)

    def map_get_data_to_user(self, data):
        result                = {}
        
        # set key and value pair first
        result[data["mykey"]] = data["value"]
        
        # convert created_at time into unit timestamp and assign into json object
        result["timestamp"]   = self.get_unix_timestamp_from_datetime(data["created_at"])

        return result

    def get_unix_timestamp_from_datetime(self, datetime_data):
        datetime_format = '%Y-%m-%dT%H:%M:%S'

        datetime_object = datetime.strptime(datetime_data, datetime_format)

        return int(time.mktime(datetime_object.timetuple()))
