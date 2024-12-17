from django.core.management.base import BaseCommand
from ...models import Shares, user_trades, userwallet  # Import your models correctly
import time
from decimal import Decimal
import threading
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User



class Command(BaseCommand):
    def update_trade(self, user_trade):
        while True:
            current_time = timezone.now()

            # Calculate the end time based on the start date and the duration in seconds
            end_time = user_trade.date + timedelta(seconds=user_trade.end_time)

            # Debug: Print the current time and end time to check
            self.stdout.write(f"Current Time: {current_time}, End Time: {end_time}")

            if current_time > end_time:
                self.stdout.write(f"End time reached for {user_trade.name}. Stopping updates.")

                # Add the final user_trade value to the user's wallet
                try:
                    user_wallet = userwallet.objects.get(user=user_trade.user)
                    user_wallet.amount += float(user_trade.value)  # Add the final value of the trade
                    user_wallet.save()
                    self.stdout.write(f"Updated wallet for user {user_trade.user.username}: New amount is {user_wallet.amount}")
                except userwallet.DoesNotExist:
                    self.stdout.write(f"UserWallet does not exist for user {user_trade.user.username}")

                break  # Exit the loop if the end time is reached

            # Debugging the calculation of percentage profit
            increment_value = user_trade.value * (user_trade.percentage / Decimal(100))
            self.stdout.write(f"Current Value: {user_trade.value}, Percentage: {user_trade.percentage}, Increment: {increment_value}")

            # Apply the increment to the value
            user_trade.value += increment_value
            user_trade.save()
            # Debugging the updated value
            self.stdout.write(f"Updated Value: {user_trade.value}")

            # Sleep for the interval defined in the model (in seconds)
            time.sleep(user_trade.update_interval)

    def handle(self, *args, **kwargs):
        # Fetch all user trades
        trades = user_trades.objects.all()
        threads = []

        for trade in trades:
            # Start a new thread for each trade update
            thread = threading.Thread(target=self.update_trade, args=(trade,))
            thread.daemon = True  # Allow thread to exit when main program exits
            threads.append(thread)
            thread.start()

        # Keep the main thread alive to allow all threads to run
        while True:
            time.sleep(1)