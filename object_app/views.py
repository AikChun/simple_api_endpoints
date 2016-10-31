from .serializers import GenericObjectSerializer
from .models import GenericObject
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from datetime import datetime
from rest_framework.renderers import JSONRenderer
# Create your views here.

class GenericObjectList(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    
    #def get(self, request, format=None):
    #    queryset   = GenericObject.objects.all()
    #    serializer = GenericObjectSerializer(queryset, many=True)
    #    return Response(serializer.data)
    
    def post(self, request, format=None):
        #request.data['timestamp'] = datetime.utcfromtimestamp(int(request.data['timestamp'])).isoformat()
        serializer = GenericObjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenericObjectDetail(APIView):
    """
    Retrieve a GenericObject instance.
    """
    renderer_classes = (JSONRenderer, )
    def get(self, request, mykey, format=None):
        queryset = GenericObject.objects.filter(mykey=mykey)

        timestamp = self.request.query_params.get('timestamp', None)
        if timestamp is not None:
            timestamp = datetime.utcfromtimestamp(int(timestamp)).isoformat()
            queryset = queryset.filter(created_at__lte=timestamp)

        if not queryset.count():
            raise Http404

        queryset = queryset.order_by('-created_at')[0]

        serializer = GenericObjectSerializer(queryset)

        return Response(serializer.data)
