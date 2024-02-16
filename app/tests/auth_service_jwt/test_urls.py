import pytest
from django.urls import resolve, reverse
from auth_service_jwt.views import SignUpAPIView, LoginAPIView, LogoutAPIView, TokenRefreshView


@pytest.mark.django_db
def test_signup_url():
    resolver = reverse('signup')
    assert resolve(resolver).func.view_class == SignUpAPIView


@pytest.mark.django_db
def test_login_url():
    resolver = reverse('login')
    assert resolve(resolver).func.view_class == LoginAPIView


@pytest.mark.django_db
def test_logout_url():
    resolver = reverse('logout')
    assert resolve(resolver).func.view_class == LogoutAPIView


@pytest.mark.django_db
def test_token_refresh_url():
    resolver = reverse('token_refresh')
    assert resolve(resolver).func.view_class == TokenRefreshView