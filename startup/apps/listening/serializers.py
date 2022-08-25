from rest_framework import serializers
from .models import Listening, Question, Like, Variant

"""This serializers is for list Listening!"""


class VariantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'variant']
        ref_name = 'listening_variant'


class QuestionListSerializer(serializers.ModelSerializer):
    variants = VariantListSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'variants']
        ref_name = 'listening_question'


class ListeningListSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(many=True)
    views = serializers.IntegerField(read_only=True)
    likes = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return Like.objects.filter(listening=obj).all().count()

    class Meta:
        model = Listening
        fields = ['id', 'title', 'audio', 'type', 'background', 'likes', 'views', 'questions']
