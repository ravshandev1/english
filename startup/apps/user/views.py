from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status, permissions, exceptions
from rest_framework.response import Response
from .serializers import UserListSerializer, RegisterSerializer, LoginSerializer, ForgetPasswordSerializer, \
    SetPasswordSerializer, ChangePasswordSerializer, RetrieveSerializer
from .models import User
from .utils import SendEmail
from django.conf import settings


class UserListAPIView(generics.ListAPIView):
    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return UserListSerializer


class RegisterAPIView(generics.CreateAPIView):
    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return RegisterSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return RetrieveSerializer


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        data = serializer.data
        data['id'] = User.objects.filter(username=username).first().id
        data['education'] = User.objects.filter(username=username).first().education
        return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)


class ForgetPasswordAPIView(generics.GenericAPIView):

    def get_serializer_class(self):
        return ForgetPasswordSerializer

    def post(self, request):
        user = User.objects.filter(username=request.data['username']).first()

        if user:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = settings.CURRENT_SITE
            abs_url = f'{current_site}/user/set-password?uidb64={uidb64}&token={token}'
            email_body = f'Hello \n Use link below at reset password \n {abs_url}'
            data = {
                'to_email': request.data['email'],
                'email_subject': 'Reset password',
                'email_body': email_body
            }
            SendEmail.send_email(data)
            return Response({'success': True, 'message': 'Link sent to email'}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Username is not correct'}, status=status.HTTP_400_BAD_REQUEST)


class SetPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Successfully password changed!'})


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        username = request.user.username
        old_password = request.data['old_password']
        user = authenticate(username=username, password=old_password)
        if not user:
            raise exceptions.AuthenticationFailed({'message': 'Password is not correct'})
        else:
            serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = request.data['password']
        user.set_password(password)
        user.save()
        return Response({'success': True, 'message': 'Successfully password changed!'})
