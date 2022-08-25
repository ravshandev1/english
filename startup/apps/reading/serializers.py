from rest_framework import serializers
from .models import Question, Reading, Like, Variant

"""This serializer is for list Reading!"""


class VariantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'variant']


class QuestionListSerializer(serializers.ModelSerializer):
    variants = VariantListSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'variants']


class ReadingListSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return Like.objects.filter(reading=obj).all().count()

    class Meta:
        model = Reading
        fields = ['id', 'title', 'text', 'type', 'background', 'likes', 'views', 'questions']
