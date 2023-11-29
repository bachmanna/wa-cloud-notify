# yourapp/urls.py
from django.urls import path
from .views import WhatsAppMessageView

urlpatterns = [
    path('send-whatsapp/', WhatsAppMessageView.as_view(), name='send_whatsapp'),
]
