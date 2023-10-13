from django.db import models
from django.contrib.auth.models import AbstractUser

from .encryption import AESCipher
# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    hashed_mobile_number = models.CharField(max_length=100, unique=True)

    @property
    def mobile_number(self):
        decrypted_mobile = AESCipher().decrypt(self.hashed_mobile_number)
        return decrypted_mobile
    
    @classmethod
    def fetch_user_with_mobile(cls, mobile):
        encrypted_mobile = AESCipher().encrypt(mobile)
        obj = User.objects.filter(hashed_mobile_number = encrypted_mobile).first()
        return obj
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.hashed_mobile_number = AESCipher().encrypt(self.hashed_mobile_number)

        super(User, self).save(*args, **kwargs)
        
    REQUIRED_FIELDS = ['hashed_mobile_number']