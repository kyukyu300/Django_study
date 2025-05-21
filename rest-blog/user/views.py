from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer


# Create your views here.

class SignUpAPIView(CreateAPIView):
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # refresh = RefreshToken.for_user(serializer.instance)
        #
        # response_data = {"refresh": str(refresh), "access": str(refresh.access_token)}

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)