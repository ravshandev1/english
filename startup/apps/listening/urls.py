from django.urls import path
from .views import ListeningListAPIView, ListeningRetrieveAPIView, LikeCreateAPIView, QuestionAPIView

urlpatterns = [
    path('', ListeningListAPIView.as_view()),
    path('like/', LikeCreateAPIView.as_view()),
    path('<int:pk>/', ListeningRetrieveAPIView.as_view()),
    path('quiz/', QuestionAPIView.as_view()),
]
