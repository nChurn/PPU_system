from rest_framework import serializers
from app_models.models import VnedPPU

class VnedPPUSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = VnedPPU