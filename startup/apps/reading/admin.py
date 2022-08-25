from django.contrib import admin
from .models import Reading, Question, Like, Variant


# Register your models here.
class VariantInline(admin.StackedInline):
    model = Variant
    extra = 0
    fieldsets = (
        ('Variant', {
            'fields': (('variant',),)
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [VariantInline]
    list_display = ['id', 'reading', 'question', 'answer']


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type', 'views', 'likes']
    fields = ['title', 'text', 'type', 'background']

    def likes(self, obj):
        return Like.objects.filter(reading=obj).all().count()


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'reading']
