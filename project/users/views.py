from django.shortcuts import render
from django.core.cache import cache

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .serializers import UserSerializer
from .exceptions import InvalidMobileNumberException, InvalidOtpException
import random, requests, phonenumbers

# Create your views here.

class RegisterUser(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['generate_otp', 'verify_otp']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @action(detail=False, methods=['POST'])
    def generate_otp(self, request, *args, **kwargs):
        request_body = request.data
        mobile = request_body.get('mobile')
        mobile_validation = phonenumbers.is_valid_number(phonenumbers.parse(mobile))

        if not mobile_validation:
            raise InvalidMobileNumberException

        user = User.fetch_user_with_mobile(mobile=mobile)
        if user is None:
            user = User.objects.create(username=mobile, hashed_mobile_number = mobile)
        
        cache.set(mobile, '00000')
        return Response({
            "success": True,
            "otp" : '00000',
            "user" : self.get_serializer(user).data
        })
    
    @action(detail=False, methods=['POST'])
    def verify_otp(self, request, *args, **kwargs):
        request_body = request.data
        mobile = request_body.get('mobile')
        otp = request_body['otp']
        generated_otp = cache.get(mobile)

        user = User.fetch_user_with_mobile(mobile)
        if user is None:
            return Response({
                "success": False,
                "message": "kindly register "
            })
        
        if otp == generated_otp:
            cache.delete(mobile)
            
            return Response({
                "success": True,
                "user" :self.get_serializer(user).data
            })
        
        raise InvalidOtpException
        
        
    @action(detail=False, methods=['POST'])
    def success(self, request, *args, **kwargs):
        # request_body = request.data
        # mobile = request_body.get('mobile')
        # user = User.objects.filter(username=mobile).first()
        # if user is None:
        #     user = User.objects.create(username = mobile)

        user = request.user
        return Response({
            "use" : user.username
            # "user" : self.get_serializer(user).data
        })
