from django.db.models import Model, CASCADE, CharField, BooleanField, DecimalField, EmailField, ForeignKey, IntegerField
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise TypeError('Username did not come')
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **kwargs):
        if not password:
            raise TypeError('Password did not come')
        user = self.create_user(username, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser, PermissionsMixin):
    username = CharField(max_length=255, unique=True)
    email = EmailField(unique=True, null=True, blank=True)
    education = CharField(max_length=255, null=True, blank=True)
    score = DecimalField(max_digits=4, decimal_places=1, default=0.0)
    is_superuser = BooleanField(default=False)
    is_staff = BooleanField(default=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Payment(Model):
    user = ForeignKey(User, CASCADE)
    payment_value = IntegerField()

    def __str__(self):
        return f"User: {self.user.username} payment: {self.payment_value}"
