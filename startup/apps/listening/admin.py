from django.contrib import admin
from .models import Listening, Question, Like, Variant


# Register your models here.
class VariantInline(admin.StackedInline):
    model = Variant
    extra = 0
    fieldsets = (
        ('Variant', {
            'fields': (('variant',),)
        }),
    )


@admin.register(Listening)
class ListeningAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type', 'views', 'likes']
    fields = ['title', 'audio', 'type', 'background']

    def likes(self, obj):
        return Like.objects.filter(listening=obj).all().count()


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [VariantInline]
    list_display = ['id', 'listening', 'question', 'answer']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'listening']
