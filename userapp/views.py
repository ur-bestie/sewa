import requests
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.utils.safestring import mark_safe
from django.views import View
from django.conf import settings
import json
from django.urls import reverse
from django.templatetags.static import static
from .forms import *

# Create your views here.
def index(request):
    return render(request,'home/index.html')

def login(request):
    if request.method == 'POST':
       email = request.POST.get('email')
       password = request.POST.get('password')


       user = authenticate(request, email=email, password=password)
       if user is not None:
          auth_login(request, user)
          return redirect('/user')
       else:
          messages.error(request,'Email or password not correct')
          return redirect('/login')
    return render(request,'auth/login.html')


def register(request):
     if request.method == 'POST':  
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name') 
        username = request.POST.get('username') 
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')  
        if password == password2:
          if CustomUser.objects.filter(username=username).exists():
             messages.error(request,'Username Already Exists')
             return redirect('/register')
          elif CustomUser.objects.filter(email=email).exists():
            messages.error(request,'Email already in use')
            return redirect('/register')
          else:
             hashed_password = make_password(password)
             user = CustomUser(first_name=first_name,last_name=last_name,username=username, email=email, password=hashed_password)
             user.save()
             return redirect('/login')
        else:    
         messages.error(request,'password not the same')
         return redirect('/register')  
     else:
        return render(request,'auth/register.html')

def logout(request):
   auth.logout(request)
   return redirect('/')

@login_required
def user(request):
   user = request.user
   acc = userwallet.objects.get_or_create(user=user,currency='$')
   x = userwallet.objects.filter(user=user).first
   return render(request,'user/dashboard.html', locals())
   

@login_required
def deposit(request):
   x = paymentmethod.objects.all()
   return render(request,'user/deposit.html', locals())

@login_required
def depositam(request, id):
   x = paymentmethod.objects.get(id=id)
   return render(request,'user/depositam.html', locals())

@login_required
def depositconf(request):
   user=request.user
   p_id = request.GET.get('p_id')
   amount = request.GET.get('amount')
   x = paymentmethod.objects.get(pk=p_id)
  

   if request.method == 'POST':
      proof =  request.FILES.get('proof')
      address = request.POST.get('address')

      dc = deposit_his.objects.create(user=request.user,paymentm=x,amount=amount,address=address,proof=proof)
   
      messages.success(request,'you have made a deposit')
      return redirect('/user')
   else:
    return render(request,'user/depositconf.html', locals())

def deposithis(request):
   x = deposit_his.objects.filter(user=request.user)
   return render(request,'user/deposithis.html', locals())

def assets(request):
   user = request.user
   x = asset.objects.all()
   if request.method == 'POST':
      amount = request.POST.get('amount')
      a_id = request.POST.get('a_id')
      
      ax = asset.objects.get(pk=a_id)
      ba = userwallet.objects.get(user=user)
      if float(amount) > ba.amount:
         messages.error(request,'insuficiant funds')
         return redirect('/assets')
      else:
         ab = assetbuy.objects.create(user=user,asset=ax,amount=amount)
         ab.save()
         ba.amount -= float(amount)
         ba.save()
         messages.success(request, 'asset bought successfully')
         return redirect('/user')
   else:
    return render(request,'user/assets.html', locals())



def myassets(request):
   user = request.user
   x = assetbuy.objects.filter(user=user)
   if request.method == 'POST':
    a_id = request.POST.get('a_id')
    amount = request.POST.get('amount')

    edi = assetbuy.objects.get(id=a_id)
    edi.status = 'pending'
    edi.amount = amount
    edi.save()
    messages.success(request,'asset sold successfully waiting for buyer')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:
    return render(request,'user/myassets.html', locals())


def housepurchase(request):
   x = House.objects.all()
   return render(request,'user/housepurchase.html', locals())


def housedetails(request, id):
   x = House.objects.get(id=id)
   return render(request,'user/housedetails.html', locals())



def housebuy(request, id):
   user = request.user
   x = House.objects.get(id=id)
   # if request.method == 'POST':
   #    amount = x.price
   #    ba = userwallet.objects.get(user=user)
   #    if float(amount) > ba.amount:
   #       messages.error(request,'insuficiant funds')
   #       return redirect('/assets')
   #    else:
   #     x.save()
   #    messages.success(request, 'asset bought successfully')
   #    return redirect('/housecert')

   if request.method == 'POST':
        form = HousePurchaseForm(request.POST, request.FILES)
        amount = x.price
        ba = userwallet.objects.get(user=user)
        if float(amount) > ba.amount:
            messages.error(request,'insuficiant funds')
            return redirect('/assets')
        else:
         if form.is_valid():
            form.save()
            return redirect('success')  # Replace with the name of your success URL
         else:
          form = HousePurchaseForm()
    

   else:
    return render(request,'user/housebuy.html', locals())


def profilepage(request):
   return render(request,'user/profile.html', locals())









def about(request):
    return render(request,'home/about.html')

def blogs(request):
    return render(request,'home/blogs.html')

def faq(request):
    return render(request,'home/faq.html')

def contact(request):
    return render(request,'home/contact.html')