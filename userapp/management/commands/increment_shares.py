from django.core.management.base import BaseCommand
from ...models import user_Shares, userwallet  # Import your models correctly
import time
from decimal import Decimal
import threading

class Command(BaseCommand):
    help = 'Updates the value of user shares and updates user wallets with the cumulative increment.'

    def update_share(self, user_share, run_duration=20):
        start_time = time.time()
        total_increment = Decimal(0)  # Track total increment

        while time.time() - start_time < run_duration:
            # Calculate the increment for the current interval
            increment_value = user_share.value * (user_share.interest_rate / Decimal(100))

            # Update the share value
            user_share.value += increment_value
            user_share.save()

            # Add the increment to the cumulative total
            total_increment += increment_value

            # Log the share update
            self.stdout.write(
                f"Updated {user_share.name}: Increment = {increment_value}, New Value = {user_share.value}"
            )

            # Sleep for the update interval
            time.sleep(user_share.update_interval)

        # After updates, add the cumulative increment to the user's wallet
        try:
            user_wallet = userwallet.objects.get(user=user_share.user)
            user_wallet.amount += float(total_increment)  # Add the total increment to the wallet
            user_wallet.save()

            # Log wallet update
            self.stdout.write(
                f"User {user_share.user.username}'s Wallet Updated: Total Increment = {total_increment}, Final Wallet Balance = {user_wallet.amount}"
            )
        except userwallet.DoesNotExist:
            self.stdout.write(f"Wallet not found for user {user_share.user.username}")

        # Log the end of the process
        self.stdout.write(f"Stopped updating {user_share.name} after {run_duration} seconds.")

    def handle(self, *args, **kwargs):
        # Fetch all user shares
        user_shares = user_Shares.objects.all()
        threads = []

        for share in user_shares:
            # Start a thread for each share update
            thread = threading.Thread(target=self.update_share, args=(share,))
            thread.daemon = True  # Allow threads to exit when the main program exits
            threads.append(thread)
            thread.start()

        # Keep the main thread alive to allow threads to run
        while True:
            time.sleep(1)
