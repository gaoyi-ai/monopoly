from django.contrib.auth.models import User
from rest_framework import serializers

from monopoly.models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class CreateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar']
        extra_kwargs = {'avatar': {'required': False, 'allow_null': True}, 'id': {'read_only': True}}

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User(username=user_data['username'])
        user.set_password(user_data['password'])
        user.save()
        profile = Profile.objects.create(user=user, avatar=validated_data['avatar'])
        return profile


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}, 'username': {'read_only': True}}

    def update(self, instance, validated_data):
        new_password = validated_data['password']
        instance.set_password(new_password)
        instance.save()
        return instance


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'avatar']
        extra_kwargs = {'avatar': {'required': False, 'allow_null': True}, 'id': {'read_only': True}}
