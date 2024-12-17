from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(CustomUser,UserAdmin)
admin.site.register(userwallet)
admin.site.register(paymentmethod)
admin.site.register(deposit_his)
admin.site.register(asset)
admin.site.register(assetbuy)
admin.site.register(withdraw_his)

class stocks_planAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'current_price', 'profit_percentage', 'loss_percentage', 'profit_active', 'profit_start_seconds', 'loss_start_seconds')
    list_editable = ('profit_percentage', 'loss_percentage', 'profit_active', 'profit_start_seconds', 'loss_start_seconds')

class compStocksAdmin(admin.ModelAdmin):
    list_display = ('current_price','transaction_type','date',)

admin.site.register(stocks_plan, stocks_planAdmin)
admin.site.register(compStocks, compStocksAdmin)


class HousePictureInline(admin.TabularInline):  # You can also use StackedInline for a different layout
    model = House.other_pictures.through  # Use the through model for ManyToMany
    extra = 3  # How many empty file upload forms to show (you can adjust this)
    verbose_name = 'Other Picture'
    verbose_name_plural = 'Other Pictures'

# Admin class for House model
@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    inlines = [HousePictureInline]  # Use inline to allow adding multiple pictures directly
    exclude = ('other_pictures',)  # Exclude the ManyToManyField since it's handled by the inline form

# Admin class for HousePicture
@admin.register(HousePicture)
class HousePictureAdmin(admin.ModelAdmin):
    pass

admin.site.register(housebuy)
admin.site.register(HousePurchaseInfo)
admin.site.register(Stock_user)
admin.site.register(tradeplan)
admin.site.register(user_trades)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_balance', 'percentage_increase', 'percentage_decrease', 'increase_interval', 'decrease_interval')

#house rent
class HouseforrentPicturesInline(admin.TabularInline):  # You can also use StackedInline for a different layout
    model = Houseforrent.rentother_pictures.through  # Use the through model for ManyToMany
    extra = 3  # How many empty file upload forms to show (you can adjust this)
    verbose_name = 'Other Picture'
    verbose_name_plural = 'Other Pictures'

# Admin class for House model
@admin.register(Houseforrent)
class HouseforrentAdmin(admin.ModelAdmin):
    inlines = [HouseforrentPicturesInline]  # Use inline to allow adding multiple pictures directly
    exclude = ('other_pictures',)  # Exclude the ManyToManyField since it's handled by the inline form

# Admin class for HousePicture
@admin.register(HouseforrentPictures)
class HouseforrentPicturesAdmin(admin.ModelAdmin):
    pass

admin.site.register(RentalApplication)
admin.site.register(houserentconfir)
admin.site.register(newsletter)
@admin.register(Shares)
class SharesAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'interest_rate']

@admin.register(user_Shares)
class user_SharesAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'interest_rate']