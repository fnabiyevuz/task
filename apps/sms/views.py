from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SendSMSSerializer
from .utils import send_sms


class SendSmsAPIView(APIView):

    @swagger_auto_schema(request_body=SendSMSSerializer)
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        message = request.data.get('message')

        if message and phone:
            success = send_sms(message, phone)

            if success:
                return Response(
                    {
                        'status': 'succes',
                        'message': 'SMS sent successfully.'
                    }, status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {
                        'status': 'error',
                        'code': 'providers_are_not_working',
                        'message': 'Sms providers are not working'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            {
                'status': 'error',
                'code': 'phone_and_message_required',
                'message': 'phone and message are required.'
            }, status=status.HTTP_400_BAD_REQUEST
        )
