from django.db import models

from users.models import User
# Create your models here.

class BotModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200, blank=True, null=True)
    file = models.FileField(upload_to='media/', blank=True, null=True)
    file_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    