import timedelta

from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from twilio.request_validator import RequestValidator

from .models import Message, UserProfile
from .tasks import process_offline_messages


# Create your views here.


@csrf_exempt
def receive_whatsapp_message(request):
    if request.method == 'POST':
        # validate twilio webhook
        validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

        # extract message details
        sender = request.POST.get('From')
        message_body = request.POST.get('Body')
        message_sid = request.POST.get('MessageSid')

        # find recipient user
        try:
            recipient_profile = UserProfile.objects.get(whatsapp_number = sender)

            # create message record
            message = Message.objects.create(
                user = recipient_profile.user,
                sender_number = sender,
                message_content = message_body,
                whatsapp_message_id = message_sid
            )

            # if user is offline trigger email process
            if not recipient_profile.is_online:
                process_offline_messages.delay()
            return JsonResponse({'status': 'success'})

        except UserProfile.DoesNotExist:
            return JsonResponse({'status': 'user_not_found'})

    return JsonResponse({'status': 'Invalid_request'}, status = 400)

    
# def whatsapp_webhook(request):
#     if request.method == 'POST':
#         data = request.json
#         user_phone = data.get('phone_number')
#         message_content = data.get('message')

#         try:
#             user_profile = UserProfile.objects.get(user__username = user_phone)
#         except UserProfile.DoesNotExist:
#             return JsonResponse({"error": "User not found"}, status = 400)

#         # save the message
#         message = Message.objects.create(
#             sender = user_phone,
#             content = message_content,
#             user = user_profile
#         )

#         # check offline status

#         offline_threshhold = now() - timedelta(minutes=10)
#         if user_profile.last_seen < offline_threshhold and user_profile.email_forwading_enabled:
#             return JsonResponse({
#                 "status": "Message received"
#             })
#     return JsonResponse({"error": "Invalid request"}, status = 400)