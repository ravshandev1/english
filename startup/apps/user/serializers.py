from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers, exceptions
from .models import User, Payment
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'education']

    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        pas = attrs['password']
        pas2 = attrs['password2']

        if pas != pas2:
            raise serializers.ValidationError({'success': False, 'message': 'Password did not match, please try again'})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise exceptions.AuthenticationFailed({'message': 'Username or password is not correct'})
        return attrs


class RetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'education', 'score']

    score = serializers.SerializerMethodField(read_only=True)

    def get_score(self, obj):
        score = User.objects.filter(username=obj.username).first().score
        return f'{score} %'


"""This serializers is for list Users!"""


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_value']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'education', 'score', 'payment_set']

    payment_set = PaymentListSerializer(many=True, read_only=True)
    score = serializers.SerializerMethodField(read_only=True)

    def get_score(self, obj):
        score = User.objects.filter(username=obj.username).first().score
        return f'{score} %'


class ForgetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2']

    old_password = serializers.CharField(required=True, min_length=8)
    password = serializers.CharField(required=True, min_length=8)
    password2 = serializers.CharField(required=True, min_length=8)

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        if password != password2:
            raise serializers.ValidationError({'success': False, 'message': 'Password did not match, please try again'})
        return attrs


class SetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'password2', 'uidb64', 'token']

    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        uidb64 = attrs['uidb64']
        token = attrs['token']
        _id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.filter(id=_id).first()
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise exceptions.AuthenticationFailed({'success': False, 'message': 'The reset link is invalid'})
        if password != password2:
            raise serializers.ValidationError({'success': False, 'message': 'Password did not match, please try again'})
        user.set_password(password)
        user.save()
        return attrs
