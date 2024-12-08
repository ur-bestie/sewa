from django.core.management.base import BaseCommand
from django.utils.timezone import now
from userapp.models import Stock
import time

# class Command(BaseCommand):
#     help = 'Update stock balances based on increase and decrease intervals.'

#     def handle(self, *args, **kwargs):
#         self.stdout.write("Starting stock update process...")
#         while True:
#             stocks = Stock.objects.filter(running=True)
#             current_time = now()

#             for stock in stocks:
#                 time_since_last_update = (current_time - stock.last_update).total_seconds()

#                 # Apply increase if the interval has passed
#                 if time_since_last_update >= stock.increase_interval:
#                     self.apply_increase(stock)

#                 # Apply decrease if the interval has passed
#                 if time_since_last_update >= stock.decrease_interval:
#                     self.apply_decrease(stock)

#             time.sleep(1)  # Check every second

#     def apply_increase(self, stock):
#         increase_amount = stock.current_balance * (stock.percentage_increase / 100)
#         stock.current_balance += increase_amount
#         stock.last_update = now()
#         stock.save()

#     def apply_decrease(self, stock):
#         decrease_amount = stock.current_balance * (stock.percentage_decrease / 100)
#         stock.current_balance -= decrease_amount
#         stock.last_update = now()
#         stock.save()
