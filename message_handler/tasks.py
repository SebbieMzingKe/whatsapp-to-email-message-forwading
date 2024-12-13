from celery import shared_task
from .models import Message, UserProfile
from .utils import send_email_notification

@shared_task
def process_offline_messages():

    # find offline users
    offline_users = UserProfile.objects.filter(is_online = False)

    for profile in offline_users:
        # find unsynced messages of this user
        unsynced_messages = Message.objects.filter(
            user = profile.user,
            is_emailed = False
        )

        for message in unsynced_messages:
            # try to send email
            if send_email_notification(profile.user, message):
                message.is_emailed = False
                message.save()
                