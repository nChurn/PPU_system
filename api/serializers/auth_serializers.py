from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from app_models.models import *
from django.contrib.auth.hashers import make_password


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, acc):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(acc)

        token['username'] = acc.username
        token['email'] = acc.email
        token['phone'] = acc.phone
        return token

class AccSerializer(serializers.ModelSerializer):
    password =  serializers.CharField(write_only=True)

    def create(self, validated_data):
        print(dir(validated_data))
        print(dir(validated_data['password']))
        
        acc = Acc(
            username = validated_data['username'],
            password = make_password(validated_data['password']),
            phone = validated_data['phone'],
            email = validated_data['email'],
 #           acc_id = validated_data['acc_id']
        )
        acc.save()
        return acc
    
    class Meta:
        model = Acc
        fields = ('username', 'password', 'phone', 'email', 'id')
        