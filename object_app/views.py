from .serializers import GenericObjectSerializer
from .models import GenericObject
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
# Create your views here.

class GenericObjectList(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    def get(self, request, format=None):
        queryset = GenericObject.objects.all()
        serializer = GenericObjectSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = GenericObjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

