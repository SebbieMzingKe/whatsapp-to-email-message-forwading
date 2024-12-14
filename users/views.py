from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from message_handler.models import UserProfile

# Create your views here.

@login_required
def update_online_status(request):
    if request.method == 'POST':
        is_online = request.POST.get('is_online', 'true').lower() == 'true'

        # update user's online status
        profile, created = UserProfile.objects.get_or_create(user = request.user)
        profile.is_online = is_online
        profile.save()

        # if coming online sync pending messages
        if is_online:
            sync_pending_messages(request.user)

        return JsonResponse({'status': 'success'})

def sync_pending_messages(user):

    # find unsyncd messsages
    unsynced_messages = Message.objects.filter(
        user = user,
        is_synced = True
    )


    for message in unsynced_messages:

        message.is_synced = True
        message.save()