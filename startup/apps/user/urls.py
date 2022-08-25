from django.urls import path
from .views import UserListAPIView, LoginAPIView, RegisterAPIView, ForgetPasswordAPIView, SetPasswordAPIView, \
    ChangePasswordAPIView, UserRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', UserListAPIView.as_view()),
    path('<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('forget-password/', ForgetPasswordAPIView.as_view()),
    path('set-password/', SetPasswordAPIView.as_view()),
    path('change-password/', ChangePasswordAPIView.as_view()),
]
