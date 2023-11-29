from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SendMessageSerializer
from heyoo import WhatsApp
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

@api_view(['POST'])
def send_whatsapp_message(request):
    if request.method == 'POST':
        serializer = SendMessageSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Extract parameters from the validated data
            message = data['message']
            recipient_id = data['recipient_id']
            recipient_type = data.get('recipient_type', 'individual')
            preview_url = data.get('preview_url', True)

            # Initialize your WhatsApp object with the required token and phone number ID
            whatsapp = WhatsApp(token="YOUR_TOKEN", phone_number_id="YOUR_PHONE_NUMBER_ID")

            try:
                # Call the send_message function with the extracted parameters
                whatsapp.send_message(message, recipient_id, recipient_type, preview_url)
                return Response({"detail": "Message sent successfully"}, status=200)
            except Exception as e:
                return Response({"detail": f"Error sending message: {str(e)}"}, status=500)

        return Response(serializer.errors, status=400)
