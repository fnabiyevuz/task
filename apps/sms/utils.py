import json
import random
import string

import requests
from django.conf import settings

from apps.sms.models import SmsProviderType, SmsSetting, SmsLog


def send_sms(message, phone):
    sms_provider = SmsSetting.objects.first() or SmsSetting.objects.create(provider=SmsProviderType.ESKIZ)
    provider = sms_provider.provider

    if provider == SmsProviderType.ESKIZ:

        eskiz_send = send_sms_with_eskiz(phone, message)
        if eskiz_send:
            return True

        play_mobile_send = send_sms_with_play_mobile(phone, message)
        if play_mobile_send:
            return True

        get_sms_send = send_sms_with_get_sms(phone, message)
        if get_sms_send:
            return True

        return False

    elif provider == SmsProviderType.PLAY_MOBILE:

        play_mobile_send = send_sms_with_play_mobile(phone, message)
        if play_mobile_send:
            return True

        get_sms_send = send_sms_with_get_sms(phone, message)
        if get_sms_send:
            return True

        eskiz_send = send_sms_with_eskiz(phone, message)
        if eskiz_send:
            return True

        return False

    elif provider == SmsProviderType.GET_SMS:
        get_sms_send = send_sms_with_get_sms(phone, message)
        if get_sms_send:
            return True
        eskiz_send = send_sms_with_eskiz(phone, message)
        if eskiz_send:
            return True

        play_mobile_send = send_sms_with_play_mobile(phone, message)
        if play_mobile_send:
            return True

    return False


def send_sms_with_eskiz(phone, message):
    end_point = settings.ESKIZ_SEND_SMS_ENDPOINT
    sms_token = settings.ESKIZ_SMS_TOKEN
    callback_url = settings.CALLBACK_URL

    headers = {
        "Authorization": f"Bearer {sms_token}",
        "Content-Type": "application/json"
    }

    data = {
        "mobile_phone": phone,
        "message": message,
        "from": 4546,
        "callback_url": callback_url
    }

    response = requests.post(end_point, json=data, headers=headers)

    return write_sms_log(response, phone, message, SmsProviderType.ESKIZ)


def send_sms_with_play_mobile(phone, message):
    message_id = "".join(random.choices(string.ascii_letters, k=15))
    data = {
        'messages': [
            {
                'recipient': phone,
                'message-id': message_id,
                "sms": {
                    "originator": "3700",
                    "content": {"text": message}
                },
            }
        ]
    }

    response = requests.post(
        settings.PLAY_MOBILE_SEND_SMS_ENDPOINT,
        json=data,
        auth=(
            settings.PLAY_MOBILE_USERNAME,
            settings.PLAY_MOBILE_PASSWORD
        )
    )

    return write_sms_log(response, phone, message, SmsProviderType.PLAY_MOBILE)


def send_sms_with_get_sms(phone, message):
    data = {
        'login': settings.GET_SMS_USERNAME,
        'password': settings.GET_SMS_PASSWORD,
        'data': json.dumps([{
            'phone': phone,
            'text': message
        }])
    }

    response = requests.post(settings.GET_SMS_SEND_SMS_ENDPOINT, json=data)

    return write_sms_log(response, phone, message, SmsProviderType.GET_SMS)


def write_sms_log(response, phone, message, provider):
    if response.status_code == 200:
        SmsLog.objects.create(
            provider=provider,
            phone=phone,
            message=message,
            content=response.content,
            is_send=True
        )

        sms_proviver = SmsSetting.objects.first()
        if provider != sms_proviver.provider:
            sms_proviver.provider = provider
            sms_proviver.save()

        return True

    SmsLog.objects.create(
        provider=provider,
        phone=phone,
        message=message,
        content=response.content,
        is_send=False
    )

    return False
