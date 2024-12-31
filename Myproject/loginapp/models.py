from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Myuser(User):
    imagepath=models.CharField(max_length=100)
    
    class Meta:
        db_table='auth_user2'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

