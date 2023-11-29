# yourwebhookapp/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from heyoo import WhatsApp
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

messenger = WhatsApp(token="YOUR_TOKEN", phone_number_id="YOUR_PHONE_NUMBER_ID")
VERIFY_TOKEN = "test"
@csrf_exempt
def webhook_handler(request):
    if request.method == "GET":
        if request.GET.get("hub.verify_token") == VERIFY_TOKEN:
            logging.info("Verified webhook")
            return JsonResponse({"hub.challenge": request.GET.get("hub.challenge")}, status=200)
        logging.error("Webhook Verification failed")
        return JsonResponse({"detail": "Invalid verification token"}, status=400)

    # Handle Webhook Subscriptions
    data = json.loads(request.body.decode('utf-8'))  # decode the request body
    logging.info("Received webhook data: %s", data)
    changed_field = messenger.changed_field(data)

    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            name = messenger.get_name(data)
            message_type = messenger.get_message_type(data)
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )

            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
                logging.info("Message: %s", message)

                # Send a response message using Heyoo
                messenger.send_message(f"Hi {name}, nice to connect with you", mobile)

                return JsonResponse({"detail": "ok"}, status=200)

            # Add handling for other message types as needed

    return JsonResponse({"detail": "No new message"}, status=200)
