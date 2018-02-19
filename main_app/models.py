from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy

# Create your models here.

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    is_donor = models.BooleanField(default=False)
    is_org_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    location = models.CharField(max_length=100)


class OrgAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    org_name = models.CharField(max_length=100)
    org_location = models.CharField(max_length=100)
    org_bio = models.CharField(max_length=300)


class ReliefEffort(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    org_admin_id = models.ForeignKey(OrgAdmin,
    models.SET_NULL,
    blank=True,
    null=True)
    def __str__(self):
	    return self.name

class ItemRequest(models.Model):
    name = models.CharField(max_length=40)
    desc = models.CharField(max_length=100)
    is_fulfilled = models.BooleanField(default=False)
    relief_effort_id = models.ForeignKey(ReliefEffort,
    on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Donation(models.Model):
    item_request_id = models.ForeignKey(ItemRequest,
    models.SET_NULL,
    blank=True,
    null=True)
    donor_id = models.ForeignKey(Donor,
    models.SET_NULL,
    blank=True,
    null=True)
    created_at = models.DateTimeField(auto_now_add=True)
