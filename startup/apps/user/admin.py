from django.contrib import admin
from .models import User, Payment


# Register your models here.

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]
    list_display = ['id', 'username', 'email', 'education', 'score', 'payment']

    # fields = ['username', 'email', 'education', 'score']

    def payment(self, obj):
        return Payment.objects.filter(user=obj).first()


admin.site.register(Payment)
