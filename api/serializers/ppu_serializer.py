from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from app_models.models import *



class PPUSerializer(ModelSerializer):

    #file = serializers.FileField(use_url=False)
    #author = Acc.objects.get(username=serializers.CharField(max_length=63))
    #category = Category.objects.get(title=serializers.CharField(max_length=63))
    #effect = Effect.objects.get(title=serializers.CharField(max_length=63))

    class Meta:
        model = PPU
        exclude = ('file',)
        optional_fields = ['problem', 'solution', 'author', 'co_author_procent', 'category', 'effect', 'status']
    
class ModerPPUSerializer(ModelSerializer):

    class Meta:
        model = PPU
        fields = '__all__'

class PPUFileUploadSerializer(ModelSerializer):

    class Meta:
        model = PPU
        fields = ['file']


