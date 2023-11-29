# yourapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from heyoo import WhatsApp
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

class WhatsAppMessageView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            token = 'YOUR_HEYOO_TOKEN'
            phone_number = request.data.get('phone_number', '')
            message = request.data.get('message', '')

            messenger = WhatsApp(token, phone_number_id=phone_number)
            messenger.send_message(message, phone_number)

            return Response({"detail": "Message sent successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            logging.error(f"Error sending WhatsApp message: {e}")
            return Response({"detail": "Error sending WhatsApp message"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
