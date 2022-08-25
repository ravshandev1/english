from django.urls import path, include

urlpatterns = [
    path('user/', include('user.urls')),
    path('reading/', include('reading.urls')),
    path('listening/', include('listening.urls')),
]
