from django.contrib.gis.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
from django.conf import settings

class MapChoice(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Marker(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField()

    def __str__(self):
        return self.name
    
class Livestream(models.Model):
    title = models.CharField(max_length=255, default='')
    source = models.CharField(max_length=255, default='')
    type = models.CharField(max_length=255, default='', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_livestreams')
    groups = models.ManyToManyField(Group, related_name='livestreams', blank=True) 
    latest_frame = models.ImageField(upload_to='frames', blank=True, null=True) 
    is_live = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def is_public(self):
        return self.groups.filter(name="Public").exists()
    
class Viewport(models.Model):
    name = models.CharField(max_length=255, default="Viewport")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='viewports')
    livestreams = models.ManyToManyField(Livestream, related_name='viewports')
    date_created = models.DateTimeField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, username, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, username, and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=False)
    email = models.EmailField(max_length=255, unique=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, related_name='group_memberships', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin