from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import user_Shares  # Corrected model name
from datetime import datetime, timedelta
import threading
from decimal import Decimal
import time


def update_share(user_share):
    """Update a share's value at intervals until the end interval is reached."""
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=user_share.end_interval)

    while datetime.now() < end_time:
        # Ensure value and interest_rate are Decimal types
        value = Decimal(user_share.value)
        interest_rate = Decimal(user_share.interest_rate)

        # Calculate increment based on the interest rate
        increment_value = value * (interest_rate / Decimal(100))

        # Update the share value
        user_share.value = value + increment_value
        user_share.save()

        print(f"Updated {user_share.name}: New Value = {user_share.value}")

        # Sleep for the update interval before the next update
        time.sleep(user_share.update_interval)
        
        # Set the status to True after the end interval
    user_share.status = True
    user_share.save()

    print(f"Stopped updating {user_share.name} after {user_share.end_interval} seconds.")


@receiver(post_save, sender=user_Shares)  # Use the correct model here
def start_share_update(sender, instance, created, **kwargs):
    """Start the share update process when a new user_Shares is created."""
    if created:
        print(f"Starting update for new user share: {instance.name}")
        thread = threading.Thread(target=update_share, args=(instance,))
        thread.daemon = True  # Allow thread to exit when the program exits
        thread.start()
