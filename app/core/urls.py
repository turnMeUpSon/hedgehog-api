from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth_service_jwt/', include('auth_service_jwt.urls')),
]
