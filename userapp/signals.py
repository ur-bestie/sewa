from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *  # Corrected model name
from datetime import datetime, timedelta
import threading
from decimal import Decimal
import time


def update_share(user_share):
    """Update a share's value at intervals until the end interval is reached."""
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=user_share.end_interval)
    total_increment = Decimal(0)  # To track the total increment over the update duration

    initial_value = Decimal(user_share.value)  # Save the initial value

    while datetime.now() < end_time:
        # Ensure value and interest_rate are Decimal types
        value = Decimal(user_share.value)
        interest_rate = Decimal(user_share.interest_rate)

        # Calculate increment based on the interest rate
        increment_value = value * (interest_rate / Decimal(100))

        # Update the share value
        user_share.value = value + increment_value
        user_share.save()

        # Add the increment to the total increment tracker
        total_increment += increment_value

        print(f"Updated {user_share.name}: Increment = {increment_value}, New Value = {user_share.value}")

        # Sleep for the update interval before the next update
        time.sleep(user_share.update_interval)

    # After the updates, use the final value to calculate the total to add to the wallet
    final_value = Decimal(user_share.value)  # The final value after all updates
    total_to_add = final_value  # Directly add the entire final value (not just the interest)

    try:
        # Update the user wallet with the final value
        user_wallet = userwallet.objects.get(user=user_share.user)
        user_wallet.amount += float(total_to_add)  # Add the final share value (including the interest)
        user_wallet.save()

        print(f"User {user_share.user.username}'s Wallet Updated: Final Value Added = {total_to_add}, Final Wallet Balance = {user_wallet.amount}")
    except userwallet.DoesNotExist:
        print(f"Wallet not found for user {user_share.user.username}")

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





# Signal handler that will be triggered after saving a new user_trades object
@receiver(post_save, sender=user_trades)
def start_trade_update(sender, instance, created, **kwargs):
    if created:  # Ensure that this runs only when a new object is created
        # Start a new thread to update the trade value
        threading.Thread(target=run_trade_update, args=(instance,)).start()

def run_trade_update(user_trade):
    # Import the command dynamically to avoid circular imports
    from django.core.management import call_command
    
    # Call the custom command to start the update process for this user_trade
    call_command('trdae_command')



def update_stock_price():
    """Update the stock price based on profit and loss percentages, activated by time (in seconds)."""
    while True:
        # Fetch all stocks that need to be updated
        stocks = compStocks.objects.all()

        for stock in stocks:
            current_time_seconds = int(time.time())  # Get current time in seconds since epoch
            
            # Check if profit should be applied
            if (stock.stocks_plan.profit_start_seconds and 
                current_time_seconds >= stock.stocks_plan.profit_start_seconds and 
                stock.stocks_plan.profit_active):
                
                # Increase the stock price based on the profit percentage
                new_price = stock.current_price * (1 + (stock.stocks_plan.profit_percentage / Decimal(100)))
                stock.current_price = new_price
                stock.save()
                print(f"Profit applied to {stock.stocks_plan.name}: New Value = {stock.current_price}")
                
                # Optionally, deactivate profit after applying
                # stock.stocks_plan.profit_active = False
                # stock.stocks_plan.save()

            # Check if loss should be applied
            elif (stock.stocks_plan.loss_start_seconds and 
                  current_time_seconds >= stock.stocks_plan.loss_start_seconds and 
                  not stock.stocks_plan.profit_active):
                
                # Decrease the stock price based on the loss percentage
                new_price = stock.current_price * (1 - (stock.stocks_plan.loss_percentage / Decimal(100)))
                stock.current_price = new_price
                stock.save()
                print(f"Loss applied to {stock.stocks_plan.name}: New Value = {stock.current_price}")

        # Sleep for a longer period before checking again
        time.sleep(stock.stocks_plan.profit_start_seconds)  # Update every 30 seconds

def start_stock_update_thread():
    """Start the stock update thread."""
    thread = Thread(target=update_stock_price)
    thread.daemon = True  # Ensure the thread exits when the program exits
    thread.start()
