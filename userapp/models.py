from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    

class userwallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    currency = models.CharField(max_length=10)
    amount = models.FloatField(default=0.00)


class paymentmethod(models.Model):
    name = models.CharField(max_length=100)
    walletaddress = models.CharField(max_length=100)
    logo = models.FileField(upload_to='pimage/')
    pinfo = models.TextField(max_length=100)


class deposit_his(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    paymentm = models.ForeignKey(paymentmethod,on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)
    address = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    proof = models.FileField(upload_to='proof/')
    date = models.DateTimeField(blank=True,null=True,default=timezone.now)

class withdraw_his(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    paymentm = models.ForeignKey(paymentmethod,on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)
    address = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    
    date = models.DateTimeField(blank=True,null=True,default=timezone.now)


class trans_his(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    date = models.DateTimeField(blank=True,null=True,default=timezone.now)

    def __str__(self):
        return self.name

class asset(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to='assets/')
    price = models.IntegerField(default=0)


class assetbuy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    asset = models.ForeignKey(asset, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=100, default='Bought')
    date = models.DateTimeField(blank=True,null=True,default=timezone.now)


class House(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.IntegerField(default=1000)
    description = models.TextField(max_length=10000, default='mmml')
    features = models.TextField(max_length=10000)
    location_link = models.URLField(max_length=200, default='https://googlemap.com')
    main_picture = models.FileField(upload_to='house/main_pictures/')  # Main display picture
    other_pictures = models.ManyToManyField('HousePicture', related_name='houses')

    def __str__(self):
        return self.name

class HousePicture(models.Model):
    picture = models.FileField(upload_to='house/other_pictures/')  # Store multiple pictures
    caption = models.CharField(max_length=255, blank=True, null=True)  # Add this field

    
    


class HousePurchaseInfo(models.Model):
    # Personal Information
    full_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=100)
    ssn = models.CharField(max_length=20)

    # Contact Information
    current_address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    # Financial Information
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)
    bank_statements = models.FileField(upload_to='bank_statements/')
    credit_score = models.IntegerField()

    # Employment Information
    employer_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=100)
    employment_duration_years = models.IntegerField()

    # Property Details
    property_address = models.CharField(max_length=255)
    property_price = models.DecimalField(max_digits=12, decimal_places=2)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} - {self.property_address}"



class housebuy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    HousePurchaseInfo = models.ForeignKey(HousePurchaseInfo, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=100, default='Bought')
    date = models.DateTimeField(blank=True,null=True,default=timezone.now)

    def __str__(self):
        return self.user.username


# renting properties

class HouseforrentPictures(models.Model):
    picture = models.FileField(upload_to='houseforrent/rentother_pictures/')  # Store multiple pictures

    def __str__(self):
        return f"Picture {self.id}"
    


class Houseforrent(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.IntegerField(default=1000)
    description = models.TextField(max_length=10000, default='mmml')
    features = models.TextField(max_length=10000)
    main_picture = models.FileField(upload_to='houseforrent/main_pictures/')  # Main display picture
    rentother_pictures = models.ManyToManyField('HouseforrentPictures', related_name='houses')  # Fixed reference

    def __str__(self):
        return self.name
    

class RentalApplication(models.Model):
    # Previous Rental Information
    previous_rental_address = models.CharField(max_length=255)
    landlord_name = models.CharField(max_length=100)
    landlord_contact = models.CharField(max_length=50)
    reason_for_moving = models.TextField()

    # Employment Information
    job_title = models.CharField(max_length=100)
    employer_name = models.CharField(max_length=100)
    employer_contact = models.CharField(max_length=50)
    income = models.DecimalField(max_digits=12, decimal_places=2)

    # Consent
    consent = models.BooleanField(default=False)

class newsletter(models.Model):
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class houserentconfir(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Houseforrent = models.ForeignKey(Houseforrent, on_delete=models.CASCADE)
    RentalApplication = models.ForeignKey(RentalApplication, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=100, default='Bought')
    date = models.DateTimeField(blank=True,null=True,default=timezone.now)

    def __str__(self):
        return self.user.username



class Shares(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the share
    img = models.ImageField(upload_to='sharesimg')
    value = models.DecimalField(max_digits=12, decimal_places=2, default=100.00)  # Current value of the share
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=2.00)  # Interest rate in percentage
    update_interval = models.IntegerField(default=5)  # Update interval in seconds
    end_interval = models.IntegerField(default=20)

    def __str__(self):
        return f"{self.name}: {self.value}"



class user_Shares(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    shares = models.ForeignKey(Shares, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Name of the share
    amount = models.IntegerField(default=600)
    value = models.DecimalField(max_digits=12, decimal_places=2, default=100.00)  # Current value of the share
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=2.00)  # Interest rate in percentage
    update_interval = models.IntegerField(default=5)  # Update interval in seconds
    end_interval = models.IntegerField(default=20)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(blank=True,null=True,default=timezone.now)

    def __str__(self):
        return f"{self.name}: {self.value}"


class notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



