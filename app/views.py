from email import message
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from app.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
# Create your views here.

class create(APIView):
    def post(self, request, format=None):
        data = usersSerializer(data=request.data)
        if data.is_valid():
            data.save()
            return Response({"message":"User created Successfully!"}, status=200)
        # user.save()
        # return HttpResponse(status=200)
        
