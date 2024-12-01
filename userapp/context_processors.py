from .models import notification

def notifications_processor(request):
    """ Context processor to provide notifications for the current user. """
    notif = None  # Initialize notifications as None
    if request.user.is_authenticated:  # Check if the user is logged in
        try:
            notif = notification.objects.filter(user=request.user)
        except notification.DoesNotExist:
            notif = None

    return {'notifications': notif}  # Return notifications to be available globally
