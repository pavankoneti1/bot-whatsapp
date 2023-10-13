from rest_framework.serializers import ModelSerializer
from .models import BotModel

class BotSerializer(ModelSerializer):
    class Meta:
        model = BotModel
        fields = ('id', 'message', 'file')
        