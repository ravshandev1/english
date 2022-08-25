from django.db.models import CASCADE, CharField, Model, ForeignKey, ImageField, IntegerField, FileField
from django.conf import settings


class Listening(Model):
    title = CharField(max_length=1000)
    audio = FileField(upload_to='listening')
    type = CharField(max_length=255)
    background = ImageField(upload_to='listening', null=True)
    views = IntegerField(default=0)

    def __str__(self):
        return self.title


class Question(Model):
    listening = ForeignKey(Listening, CASCADE, 'questions')
    question = CharField(max_length=1000)
    answer = CharField(max_length=1000)

    def __str__(self):
        return f"question of {self.listening.title}"


class Like(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, 'listening_like')
    listening = ForeignKey(Listening, CASCADE)

    def __str__(self):
        return f"{self.user} click like to {self.listening.title}"


class Variant(Model):
    question = ForeignKey(Question, CASCADE, 'variants')
    variant = CharField(max_length=1000)

    def __str__(self):
        return f"variant of {self.question}"
