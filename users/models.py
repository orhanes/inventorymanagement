from django.contrib.auth.models import User
from django.db import models
from common.models import Department, Position

class Profile(models.Model):
    
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, blank=True)
    firstname = models.CharField(max_length=200, blank=True)
    lastname = models.CharField(max_length=200, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
