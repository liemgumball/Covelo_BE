from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import *


class ClientSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser,
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def create(self, validated_data):
        client = CustomUser.objects.create_user(**validated_data)
        return client


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class FCMTokenSerializer(serializers.Serializer):
    user = serializers.CharField()
    fcm_token = serializers.CharField()

    def create(self, validated_data):
        user_id = validated_data['user']
        fcm_token = validated_data['fcm_token']

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid user ID")

        instance, _ = FCMToken.objects.get_or_create(
            user=user, defaults={'fcm_token': fcm_token})
        return instance

    def update(self, instance, validated_data):
        instance.fcm_token = validated_data.get(
            'fcm_token', instance.fcm_token)
        instance.save()
        return instance
