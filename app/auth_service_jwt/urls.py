from django.urls import path
from .views import SignUpAPIView, LoginAPIView, LogoutAPIView, TokenRefreshView, PingAPIView


urlpatterns = [
    path('v1/signup/', SignUpAPIView.as_view(), name='signup'),
    path('v1/login/', LoginAPIView.as_view(), name='login'),
    path('v1/logout/', LogoutAPIView.as_view(), name='logout'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/ping/', PingAPIView.as_view(), name='ping'),
]