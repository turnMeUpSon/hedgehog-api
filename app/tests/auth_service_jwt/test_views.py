import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from auth_service_jwt.serializers import CustomUserSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
def test_valid_signup():
    client = APIClient()
    url = reverse('signup')
    valid_data = {
        'username': 'test_user',
        'password': 'TestPassword123',
        'password2': 'TestPassword123'
    }
    response = client.post(url, valid_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_invalid_signup():
    client = APIClient()
    url = reverse('signup')
    invalid_data = {
        'username': 'GoodBro',
        'password': 'password1234'
    } 
    response = client.post(url, invalid_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_valid_login():
    User.objects.create_user(username='test_user', password='TestPassword123')
    client = APIClient()
    url = reverse('login')
    valid_data = {
        'username': 'test_user',
        'password': 'TestPassword123'
    }
    response = client.post(url, valid_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'username' in response.data
    assert 'tokens' in response.data


@pytest.mark.django_db
def test_invalid_login():
    User.objects.create_user(username='test_user', password='TestPassword123')
    client = APIClient()
    url = reverse('login')
    invalid_data = {
        'username': 'wrong_test_user',
        'password': 'WrongPassword1234'
    }
    missing_username = {
        'password': 'TestPassword123'
    }
    missing_password = {
        'username': 'test_user'
    }
    
    # Invalid username and password
    response1 = client.post(url, invalid_data, format='json')
    assert response1.status_code == status.HTTP_400_BAD_REQUEST

    # Missing field with username
    response2 = client.post(url, missing_username, format='json')
    assert response2.status_code == status.HTTP_400_BAD_REQUEST

    # Missing field with password
    response3 = client.post(url, missing_password, format='json')
    assert response3.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_logout_authenticated_user():
    user = User.objects.create_user(username='test_user', password='TestPassword123')
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('logout')
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK

    # Check if the user is marked as inactive
    user.refresh_from_db()
    assert not user.is_active
    assert response.data.get('message') == "Logout successful"


@pytest.mark.django_db
def test_invalid_logout():
    client = APIClient()
    url = reverse('logout')
    response = client.post(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Ensure that the user is not logged out (i.e., their `is_active` status remains unchanged)
    assert not User.objects.exists()

    # Ensure that the response does not contain the logout message
    assert 'message' not in response.data