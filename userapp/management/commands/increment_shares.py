from django.core.management.base import BaseCommand
from ...models import Shares, user_Shares  # Import your models correctly
import time
from decimal import Decimal
import threading


class Command(BaseCommand):
    help = 'Increments the value of each share based on its interest rate and update interval.'

    def update_share(self, user_share):
        while True:
            # Calculate increment based on the interest rate
            increment_value = user_share.value * (user_share.interest_rate / Decimal(100))

            # Update the share value
            user_share.value += increment_value
            user_share.save()

            # Log the update
            self.stdout.write(f"Updated {user_share.name}: New Value = {user_share.value}")

            # Sleep for the specified update interval
            time.sleep(user_share.update_interval)

    def handle(self, *args, **kwargs):
        # Fetch all user shares
        user_shares = user_Shares.objects.all()
        threads = []

        for share in user_shares:
            # Start a new thread for each share update
            thread = threading.Thread(target=self.update_share, args=(share,))
            thread.daemon = True  # Allow thread to exit when main program exits
            threads.append(thread)
            thread.start()

        # Keep the main thread alive to allow all threads to run
        while True:
            time.sleep(1)
