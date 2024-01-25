from django.urls import path

from .views import SendSmsAPIView

urlpatterns = [
    path("send/", SendSmsAPIView.as_view()),
]
