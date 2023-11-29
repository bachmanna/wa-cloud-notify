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

            elif message_type == "interactive":
                message_response = messenger.get_interactive_response(data)
                intractive_type = message_response.get("type")
                message_id = message_response[intractive_type]["id"]
                message_text = message_response[intractive_type]["title"]
                logging.info(f"Interactive Message; {message_id}: {message_text}")
                return JsonResponse({"detail": "ok"}, status=200)

            elif message_type == "location":
                message_location = messenger.get_location(data)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                logging.info("Location: %s, %s", message_latitude, message_longitude)
                return JsonResponse({"detail": "ok"}, status=200)

            elif message_type == "image":
                image = messenger.get_image(data)
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = messenger.query_media_url(image_id)
                image_filename = messenger.download_media(image_url, mime_type)
                print(f"{mobile} sent image {image_filename}")
                logging.info(f"{mobile} sent image {image_filename}")
                return JsonResponse({"detail": "ok"}, status=200)

            elif message_type == "video":
                video = messenger.get_video(data)
                video_id, mime_type = video["id"], video["mime_type"]
                video_url = messenger.query_media_url(video_id)
                video_filename = messenger.download_media(video_url, mime_type)
                print(f"{mobile} sent video {video_filename}")
                logging.info(f"{mobile} sent video {video_filename}")
                return JsonResponse({"detail": "ok"}, status=200)

            elif message_type == "audio":
                audio = messenger.get_audio(data)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = messenger.query_media_url(audio_id)
                audio_filename = messenger.download_media(audio_url, mime_type)
                print(f"{mobile} sent audio {audio_filename}")
                logging.info(f"{mobile} sent audio {audio_filename}")
                return JsonResponse({"detail": "ok"}, status=200)

            elif message_type == "document":
                file = messenger.get_document(data)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = messenger.query_media_url(file_id)
                file_filename = messenger.download_media(file_url, mime_type)
                print(f"{mobile} sent file {file_filename}")
                logging.info(f"{mobile} sent file {file_filename}")
                return JsonResponse({"detail": "ok"}, status=200)
            else:
                print(f"{mobile} sent {message_type} ")
                print(data)
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")

    return JsonResponse({"detail": "No new message"}, status=200)
