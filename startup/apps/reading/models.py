from django.db.models import Model, ForeignKey, CharField, CASCADE, TextField, IntegerField, ImageField
from django.conf import settings


class Reading(Model):
    title = CharField(max_length=1000)
    text = TextField()
    type = CharField(max_length=255)
    background = ImageField(upload_to='reading')
    views = IntegerField(default=0)

    def __str__(self):
        return self.title


class Question(Model):
    reading = ForeignKey(Reading, CASCADE, 'questions')
    question = CharField(max_length=1000)
    answer = CharField(max_length=1000, null=True)

    def __str__(self):
        return f"question of {self.reading.title}"


class Like(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, CASCADE, 'reading_like')
    reading = ForeignKey(Reading, CASCADE, 'likes')

    def __str__(self):
        return f"{self.user} click like to {self.reading.title}"


class Variant(Model):
    question = ForeignKey(Question, CASCADE, 'variants')
    variant = CharField(max_length=1000)

    def __str__(self):
        return f"variant of {self.question}"

