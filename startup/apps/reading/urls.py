from django.urls import path
from .views import ReadingListAPIView, ReadingRetrieveAPIView, LikeCreateAPIView, QuestionAPIView

urlpatterns = [
    path('', ReadingListAPIView.as_view()),
    path('like/', LikeCreateAPIView.as_view()),
    path('<int:pk>/', ReadingRetrieveAPIView.as_view()),
    path('quiz/', QuestionAPIView.as_view()),
]
