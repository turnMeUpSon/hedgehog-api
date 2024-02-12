from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from typing import Any, Dict


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})


    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password2']


    def validate_password(self, password: str) -> str:
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        has_digit = any(char.isdigit() for char in password)

        if not (has_upper and has_lower and has_digit):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter, one lowercase letter, and one number"
            )
              
        return password
    

    def validate(self, data: dict) -> dict:
        if data['password'] != data['password2']:
            raise serializers.ValidationError("The two passwords must match.")
        
        # Validate password complexity using custom validation method
        self.validate_password(data['password'])
        return data


    def create(self, validated_data: dict) -> CustomUser:
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


    class Meta:
        model = CustomUser
        fields = ['username', 'password']


    def validate(self, data: dict) -> dict:
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None or password is None:
            raise serializers.ValidationError('Must include "username" and "password".')
        
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid username or password.')
        
        return {
            'username': user.username,
            'tokens': self.get_tokens_for_user(user)
        }
    
    
    def get_tokens_for_user(self, user: CustomUser) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }