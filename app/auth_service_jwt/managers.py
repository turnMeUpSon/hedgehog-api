from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username: str, password: str):
        from .models import CustomUser

        if not username:
            raise ValueError(_("Username must be set"))
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, username: str, password: str):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user