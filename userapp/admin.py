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