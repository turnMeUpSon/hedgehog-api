import pytest
from auth_service_jwt.models import CustomUser
from django.utils import timezone


@pytest.mark.django_db
def test_custom_user_model():
    user = CustomUser.objects.create(username='user1')

    # Check if the user is created successfully
    assert user.username == 'user1'
    assert user.is_staff == False
    assert user.is_active == True
    assert user.date_joined.date() == timezone.now().date()


@pytest.mark.django_db
def test_custom_user_str_method():
    # Create a CustomUser object
    user = CustomUser.objects.create(username='user1')

    # Check if the __str__ method returns the username
    assert str(user) == 'user1'