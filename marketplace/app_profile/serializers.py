# from rest_framework import serializers
# from .models import Profile, User, Avatar
#
#
# class SignUpSerializer(serializers.ModelSerializer):
#     """
#     Сериализатор для вью регистрации
#     """
#     class Meta:
#         model = User
#         fields = ('name', 'username', 'password')
#
# class UserAuthSerializer(serializers.ModelSerializer):
#     """
#     Сериализатор для вью аутентификации
#     """
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#
# class AvatarSerializer(serializers.ModelSerializer):
#     src = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Avatar
#         fields = ['src', 'alt']
#
#     def get_src(self, obj):
#         return obj.src.url
# class ProfileSerializer(serializers.ModelSerializer):
#     """
#     Сериализатор для получени и изменения профиля
#     """
#     avatar = AvatarSerializer()
#
#     class Meta:
#         model = Profile
#         fields = ('fullName', 'email', 'phone', 'avatar')

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Avatar


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'username', 'password'


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = 'src', 'alt'


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(many=False, required=False)

    class Meta:
        model = Profile
        fields = '__all__'

class UserPasswordChangeSerializer(serializers.ModelSerializer):
    """
    Сериализация пароля пользователя
    """

    class Meta:
        model = User
        fields = ['password']

class PasswordChangeSerializer(serializers.Serializer):
    passwordCurrent = serializers.CharField(required=True)
    passwordReply = serializers.CharField(required=True)
    password = serializers.CharField(required=True)