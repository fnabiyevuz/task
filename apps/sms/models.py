from django.db import models
from solo.models import SingletonModel


class SmsProviderType(models.IntegerChoices):
    ESKIZ = 1, "Eskiz"
    PLAY_MOBILE = 2, "Play Mobile"
    GET_SMS = 3, "Get Sms"


class SmsSetting(SingletonModel):
    provider = models.IntegerField(choices=SmsProviderType.choices, default=SmsProviderType.ESKIZ)


class SmsLog(models.Model):
    provider = models.IntegerField(choices=SmsProviderType.choices)
    phone = models.CharField(max_length=13)
    message = models.CharField(max_length=255)
    content = models.TextField()
    is_send = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} - {self.is_send} - {self.created_at}"

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Sms Log'
        verbose_name_plural = 'Sms Logs'
