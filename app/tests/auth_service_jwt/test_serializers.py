import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from auth_service_jwt.serializers import CustomUserSerializer, LoginSerializer
from unittest.mock import patch
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


@pytest.mark.django_db
def test_valid_custom_user_serializer():
    valid_serializer_data = {
        'username': 'user1',
        'password': 'TestPassword123',
        'password2': 'TestPassword123'
    }
    serializer = CustomUserSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    
    # Check only the expected fields in the serialized data
    expected_data = {'username': 'user1'}
    assert serializer.data == expected_data
    
    # Check validated data (including write-only fields)
    assert serializer.validated_data == valid_serializer_data
    assert serializer.errors == {}


@pytest.mark.django_db
def test_custom_user_serializer_validate_password():
    # Password is not a least 8 characters long
    data_short_password = {
        'username': 'testuser',
        'password': 'short',
        'password2': 'short'
    }
    serializer_short_password = CustomUserSerializer(data=data_short_password)
    try:
        serializer_short_password.is_valid(raise_exception=True)
    except ValidationError as e:
        assert 'Password must be at least 8 characters long' in str(e)

    # Password missing uppercase letter
    data_no_uppercase = {
        'username': 'testuser',
        'password': 'testpassword123',
        'password2': 'testpassword123'
    }
    serializer_no_uppercase = CustomUserSerializer(data=data_no_uppercase)
    try:
        serializer_no_uppercase.is_valid(raise_exception=True)
    except ValidationError as e:
        assert 'Password must contain at least one uppercase letter' in str(e)

    # Password missing lowercase letter
    data_no_lowercase = {
        'username': 'testuser',
        'password': 'TESTPASSWORD123',
        'password2': 'TESTPASSWORD123'
    }
    serializer_no_lowercase = CustomUserSerializer(data=data_no_lowercase)
    try:
        serializer_no_lowercase.is_valid(raise_exception=True)
    except ValidationError as e:
        assert 'Password must contain at least one uppercase letter, one lowercase letter, and one number' in str(e)

    # Password missing digit
    data_no_digit = {
        'username': 'testuser',
        'password': 'TestPassword',
        'password2': 'TestPassword'
    }
    serializer_no_digit = CustomUserSerializer(data=data_no_digit)
    try:
        serializer_no_digit.is_valid(raise_exception=True)
    except ValidationError as e:
        assert 'Password must contain at least one uppercase letter, one lowercase letter, and one number' in str(e)


@pytest.mark.django_db
def test_unmathcing_passwords():
    # Passwords don't match
    invalid_data = {
        'username': 'user1',
        'password': 'TestPassword123',
        'password2': 'MismatchedPassword'
    }
    serializer = CustomUserSerializer(data=invalid_data)
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as e:
        assert 'The two passwords must match' in str(e)


@pytest.mark.django_db
def test_matching_passwords():
    # Matching passwords
    data = {
        'username': 'testuser',
        'password': 'TestPassword123',
        'password2': 'TestPassword123'
    }
    serializer = CustomUserSerializer(data=data)
    
    # Check if the serializer is valid without raising any exceptions
    assert serializer.is_valid()
    
    # Check if the validated data contains the passwords
    assert serializer.validated_data['password'] == 'TestPassword123'
    assert serializer.validated_data['password2'] == 'TestPassword123'


@pytest.mark.django_db
def test_login_serializer():
    user = User.objects.create_user(username='test_user', password='TestPassword123')
    data = {
        'username': 'test_user',
        'password': 'TestPassword123'
    }
    serializer = LoginSerializer(data=data)
    assert serializer.is_valid()

    # Check if correct tokens are returned
    tokens = serializer.get_tokens_for_user(user)
    assert 'refresh' in tokens
    assert 'access' in tokens


@pytest.mark.django_db
def test_login_serializer_authentication_success():
    # Create a user
    user = User.objects.create_user(username='test_user', password='test_password')

    # Create serializer data
    data = {
        'username': user.username,
        'password': user.password
    }

    with patch('auth_service_jwt.serializers.authenticate') as mock_authenticate:
        # Set the return value of the mock authenticate method
        mock_authenticate.return_value = user

        # Initialize serializer with data
        serializer = LoginSerializer(data=data)

        # Validate serializer
        assert serializer.is_valid()

        # Check if correct tokens are returned
        tokens = serializer.get_tokens_for_user(user)
        assert 'refresh' in tokens
        assert 'access' in tokens


@pytest.mark.django_db
def test_login_serializer_invalid_username():
    # Create serializer data with invalid username
    data = {
        'username': 'non_existing_user',
        'password': 'test_password'
    }

    # Initialize serializer with data
    serializer = LoginSerializer(data=data)

    # Validate serializer
    assert not serializer.is_valid()
    assert 'Invalid username or password.' in serializer.errors['non_field_errors']


@pytest.mark.django_db
def test_login_serializer_invalid_password():
    # Create a user
    user = User.objects.create_user(username='test_user', password='test_password')

    # Create serializer data with invalid password
    data = {
        'username': user.username,
        'password': 'wrong_password'
    }

    # Initialize serializer with data
    serializer = LoginSerializer(data=data)

    # Validate serializer
    assert not serializer.is_valid()
    assert 'Invalid username or password.' in serializer.errors['non_field_errors']


@pytest.mark.django_db
def test_login_serializer_missing_fields():
    # Create serializer data with missing fields
    data = {}

    # Initialize serializer with data
    serializer = LoginSerializer(data=data)

    # Validate serializer
    assert not serializer.is_valid()
    
    # Check for missing 'username' and 'password' errors
    assert 'username' in serializer.errors
    assert 'password' in serializer.errors