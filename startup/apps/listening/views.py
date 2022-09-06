from rest_framework import permissions, views, generics, status
from rest_framework.response import Response
from user.models import User
from .models import Listening, Like, Variant, Question
from .serializers import ListeningListSerializer
from django.db.models import Q


class ListeningListAPIView(generics.ListAPIView):
    def get_queryset(self):
        return Listening.objects.all()

    def get_serializer_class(self):
        return ListeningListSerializer


class ListeningRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Listening.objects.all()

    def get_serializer_class(self):
        return ListeningListSerializer

    def get_object(self):
        instance = super().get_object()
        instance.views += 1
        instance.save()
        return super().get_object()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        for i in serializer.data['questions']:
            vs = Variant.objects.filter(question_id=i['id']).all().order_by('?').all()
            data = []
            for j in vs:
                data.append({'id': j.id, 'variant': j.variant})
            i['variants'] = data
        return Response(serializer.data)


class LikeCreateAPIView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        lis_id = request.data['listening_id']
        qs = Like.objects.filter(Q(listening_id=lis_id) and Q(user_id=user_id)).first()
        if qs:
            qs.delete()
            return Response({'message': 'Your like deleted'}, status=status.HTTP_204_NO_CONTENT)
        else:
            try:
                Like.objects.create(listening_id=lis_id, user_id=user_id)
            except:
                return Response({'error': 'Listening does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Your like added'}, status=status.HTTP_201_CREATED)


class QuestionAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = User.objects.filter(username=request.user.username).first()
        _id = request.data['listening_id']
        try:
            instance = Listening.objects.get(id=_id)
        except (Listening.DoesNotExist, Listening.MultipleObjectsReturned):
            return Response({'error': 'Listening does not exist'})
        ques_count = instance.questions.all().count()
        count = ques_count
        for (question_id, variant_id) in zip(request.data['questions_id'], request.data['variants_id']):
            try:
                qs = Question.objects.get(id=question_id)
            except (Question.DoesNotExist, Question.MultipleObjectsReturned):
                return Response({"error": "Question does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                vs = Variant.objects.get(id=variant_id)
            except Variant.DoesNotExist:
                return Response({"error": "Variant does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if qs.answer != vs.variant:
                    count -= 1
        user.score = ((count * 100 / ques_count) + float(user.score)) / 2
        user.save()
        return Response(
            {'success': True, 'correct answers': count, 'percent': count * 100 / ques_count,
             'your score': f'{user.score} %'})
