from django.shortcuts import render

from .models import BotModel
from .serializers import BotSerializer
from users.models import User

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from twilio.rest import Client
from environs import Env

import pywhatkit
import json
from datetime import datetime, date
import pyjokes

# Create your views here.

class BotViewset(viewsets.ModelViewSet):
    queryset = BotModel.objects.all()
    serializer_class = BotSerializer
    # permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def receive_message(self, request, *args, **kwargs):
        request_body = request.data
        mobile = request_body.get('From')
        mobile = mobile[9:]
        message = request_body.get('Body')
        mediaContentType = request_body.get('MediaContentType0')

        user = User.fetch_user_with_mobile(mobile=mobile)

        if user is None:
            user = User.objects.create(username = mobile, hashed_mobile_number = mobile)

        if mediaContentType is None:
            data = BotModel.objects.create(user_id = user.id, message = message)
        else:
            url = request_body.get('MediaUrl0')
            data = BotModel.objects.create(user_id = user.id, file_url = url)

        reply = Responder().Replier(message)
        request.data._mutable = True
        request.data['message'] = reply
        request.data['mobile'] = mobile

        self.send_message(request=request)
        return Response({
            "success": True,
            "message": self.get_serializer(data).data
            })
    
    @action(detail=False, methods=['POST'])
    def send_message(self, request, *args, **kwargs):
        env = Env()
        env.read_env()
        
        account_sid = env.str('account_sid') 
        auth_token = env.str('auth_token') 
        client = Client(account_sid, auth_token)

        request_body = request.data
        mobile = request_body.get('mobile')
        message = request_body.get('message')

        user = User.fetch_user_with_mobile(mobile=mobile)
        if user is None:
            user = User.objects.create(username = mobile, hashed_mobile_number = mobile)

        m = client.messages.create(
            from_ = 'whatsapp:+14155238886',
            body = message,
            # to = f'whatsapp:+919500760868',
            to = f'whatsapp:+917013811044',
        )
        
        data = BotModel.objects.create(user_id = user.id, message = message)

        return Response({
            "success" : True,
            "data" : self.get_serializer(data).data,
        })
    
    @action(detail=False, methods=['POST'])
    def send_message_from_web(self, request, *args, **kwargs):
        request_body = request.data
        mobile = request_body.get('mobile')
        message = request_body.get('message')

        pywhatkit.sendwhatmsg_instantly(mobile, message)

class Responder:
    def Replier(self, msg):
        text = ''
        msg = msg.lower()
        if 'hi' in msg:
          text = "Hello! Welcome to our WhatsApp bot. How can I assist you today?"
          text += "\nI can help you with\n"
          text += "1.know my bussiness hours\n2.ask me to tell a joke\n3.time or date\n4. Try with 'joke-<joke category>'"

        elif 'bussiness' in msg and 'hours' in msg:
          text = "I can assist you all the day"

        elif 'time' in msg:
          time = datetime.now()
          text = time.strftime("%H:%M:%S")

        elif 'date' in msg:
          text = date.today().strftime("%m/%d/%y")

        elif 'joke-' in msg:
          try:
            text = pyjokes.get_joke(category=msg[msg.index('-') + 1:])
          except Exception as e:
            text = 'No such category of joke please try another category like\n1.neural\n2.all\n3.chuck\n4.twister'

        elif 'joke' in msg:
          text = pyjokes.get_joke()

        else:
          text = "Why can't you try some of these?\n"
          text += "1.know my bussiness hours\n2.ask me to tell a joke\n3.time or date\n4. Try with 'joke-<joke category>'"

        return text