from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField(max_length=250, unique=True)
    choice = (('1', 'user'),('2', 'driver'),('3', 'admin'))
    user_type = models.CharField(max_length=10, choices=choice)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type', 'username']
 
    
    def __str__(self):
        return f'{self.email}'
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
     
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_driver')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username}'
    
    




    
