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
    list_filter = ['reading']
    list_per_page = 20


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type', 'views', 'likes']
    fields = ['title', 'text', 'type', 'background']
    list_filter = ['type']
    search_fields = ['title']
    list_per_page = 20

    def likes(self, obj):
        return Like.objects.filter(reading=obj).all().count()


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'reading']
    list_filter = ['user', 'reading']
