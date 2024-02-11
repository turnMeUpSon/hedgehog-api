from rest_framework import status
from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import CustomUserSerializer, LoginSerializer
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated


class PingAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request: HttpRequest) -> HttpResponse:
        data = {"ping": "pong!"}
        res = {
            "status": status.HTTP_200_OK,
            "data": data["ping"]
        }
        return Response(res, status=status.HTTP_200_OK)


class SignUpAPIView(APIView):
    permission_classes = [AllowAny]


    def post(self, request: HttpRequest) -> HttpResponse:
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                "status": status.HTTP_201_CREATED,
                "data": serializer.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]


    def post(self, request: HttpRequest) -> HttpResponse:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            request.user.is_active = False
            request.user.save()

        logout(request)

        # Provide a response indicating successful logout
        response_data = {
            "status": status.HTTP_200_OK,
            "message": "Logout successful",
        }
        return Response(response_data, status=status.HTTP_200_OK)


class TokenRefreshView(TokenRefreshView):
    pass