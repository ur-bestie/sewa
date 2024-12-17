import requests
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Sum
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
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.templatetags.static import static
from .forms import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now

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


@login_required
def trade(request):
  user = request.user
  x = tradeplan.objects.all()
  amount = request.POST.get('amount')
  a_id = request.POST.get('a_id')
  if request.method == 'POST':
      ba = userwallet.objects.get(user=user)
      if float(amount) > ba.amount:
         messages.error(request,'insuficiant funds make a deposit')
         return redirect('/deposit')
      else:
         ba = userwallet.objects.get(user=request.user)
         ba.amount -= float(amount)
         ba.save()
         shares_id = tradeplan.objects.get(id=a_id)
         u_s = user_trades.objects.create(
            user=user,tradeplan=shares_id,name=shares_id.name,value=amount,percentage=shares_id.percentage,update_interval=shares_id.update_interval,end_time=shares_id.end_time
         )
         messages.success(request,'trdae has started successfully')
         return redirect('/mytrade')
  else:
    return render(request, 'user/trade.html',locals())

@login_required
def mytrade(request):
  user=request.user
  try:
   x = user_trades.objects.filter(user=user)
  except:
     user_trades.DoesNotExist
     x = None
  return render(request, 'user/mytrade.html',{'x':x})

@login_required
def comp_stocks(request):
  user = request.user
  x = stocks_plan.objects.all()
  if request.method == 'POST':
     amount = request.POST.get('amount')
     a_id = request.POST.get('a_id')
     sp = stocks_plan.objects.get(id=a_id)
     cc = compStocks.objects.create(user=user,stocks_plan=sp,current_price=amount,transaction_type='buy')
     cc.save()
     messages.success(request,'stocks bought successfully')
     return redirect('stock_list')
     
  else:
   return render(request, 'user/comp_stocks.html',locals())    

@login_required
def stock_list(request):
    user = request.user
    try:
        x = compStocks.objects.filter(user=user)
    except:
       compStocks.DoesNotExist
       x = None
    if request.method == 'POST':
      amount = request.POST.get('amount')
      a_id = request.POST.get('a_id')
      sp = compStocks.objects.get(id=a_id)
      ba = userwallet.objects.get(user=request.user)
      ba.amount += float(amount)
      ba.save()
      sp.delete()
      messages.success(request,'stockes is sold successfully and has been added to your wallet balance')
      return redirect('/user')
    else:
        return render(request, 'user/stock_list.html', locals())




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
   th = trans_his.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum']
   if th is None:
    th = 0
   total_dep = deposit_his.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum']
   if total_dep is None:
    total_dep = 0

   twd = withdraw_his.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum']
   if twd is None:
     twd = 0
   try:
    notif = notification.objects.filter(user=user)
   except:
     notification.DoesNotExist
     notif = None 
   return render(request,'user/dashboard.html', locals())


def markread(request, id):
    n = notification.objects.get(id=id)
    n.status = False
    n.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def markunread(request, id):
    n = notification.objects.get(id=id)
    n.status = True
    n.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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

@login_required
def deposithis(request):
   x = deposit_his.objects.filter(user=request.user)
   return render(request,'user/deposithis.html', locals())

@login_required
def assets(request):
   user = request.user
   
   stocks = Stock.objects.all()
   if request.method == 'POST':
      amount = request.POST.get('amount')
      a_id = request.POST.get('a_id')
      
      ax = Stock.objects.get(id=a_id)
      ba = userwallet.objects.get(user=user)
      if float(amount) > ba.amount:
         messages.error(request,'insuficiant funds')
         return redirect('/assets')
      else:
         ab = Stock_user.objects.create(user=user,Stock=ax,initial_balance=amount,current_balance=amount)
         ab.save()
         messages.success(request, 'Stcoks bought successfully')
         return redirect('/stock_list')
   else:
    return render(request,'user/assets.html',{'stocks': stocks})


@login_required
def myassets(request):
   user = request.user
   if request.method == 'POST':
    a_id = request.POST.get('a_id')
    amount = request.POST.get('amount')

    edi = Stock_user.objects.get(id=a_id)
    edi.running = 'False'
    edi.save()
    ba = userwallet.objects.get(user=request.user)
    ba.amount += float(amount)
    ba.save()
    messages.success(request,'Withdrawal successful amount added to your balance')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:
    return render(request,'user/myassets.html', locals())

@login_required
def housepurchase(request):
   x = House.objects.all()
   return render(request,'user/housepurchase.html', locals())

@login_required
def housedetails(request, id):
   x = House.objects.get(id=id)
   return render(request,'user/housedetails.html', locals())


@login_required
def housebuy_view(request, id):
   user = request.user
   x = House.objects.get(id=id)
   amount = x.price
   form = HousePurchaseInfoForm(request.POST, request.FILES)
   if request.method == "POST":
        ba = userwallet.objects.get(user=user)
        if float(amount) > ba.amount:
         messages.error(request,'insuficiant funds')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
         if form.is_valid():
               house_purchase_info = form.save()
               
               # Save to housebuy
               housebuy_entry = housebuy.objects.create(
                     user=request.user,
                     house=x,
                     HousePurchaseInfo=house_purchase_info,
                     amount=x.price,
               )
               ba.amount -= float(amount)
               ba.save()
               return redirect('/properties')  # Replace with your success URL/view name
         else:
            form = HousePurchaseInfoForm()
   return render(request, 'user/housebuy.html', {'form': form,'x':x})


@login_required
def house_cert(request, id):
   user = request.user
   p = housebuy.objects.get(id=id)
   return render(request, 'user/house_cert.html',locals())

@login_required
def properties(request):
   user = request.user
   try:
      purch = housebuy.objects.filter(user=user)
   except:
      housebuy.DoesNotExist
      purch = None

   try:
      rent = houserentconfir.objects.filter(user=request.user)
   except:
      houserentconfir.DoesNotExist
      rent = None
   return render(request, 'user/properties.html',locals())



@login_required
def houserentview(request):
   x = Houseforrent.objects.all()

   return render(request,'user/houserent.html', locals())

@login_required
def houserentinfo(request, id):
   x = Houseforrent.objects.get(id=id)
   return render(request,'user/houserentinfo.html', locals())

@login_required
def houserentpay(request, id):
    # Fetch the house object, or return 404 if not found
    user = request.user
    x = get_object_or_404(Houseforrent, id=id)
    amount = x.price
    if request.method == "POST":
        form = RentalApplicationForm(request.POST)
        ba = userwallet.objects.get(user=user)
        if float(amount) > ba.amount:
         messages.error(request,'insuficiant funds')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
         if form.is_valid():
            r_s = form.save()
            houserent_pay = houserentconfir.objects.create(
                  user=request.user,
                  Houseforrent=x,
                  RentalApplication=r_s,
                  amount=x.price,
            )
            ba.amount -= float(amount)
            ba.save()
            messages.success(request,'house rent is paid successfully')
            return redirect('/properties')  # Redirect to a success page
    else:
        form = RentalApplicationForm()  # Initialize an empty form for GET requests

    return render(request, 'user/houserentpay.html', {'form': form, 'x': x})

@login_required
def rentedview(request,id):
   user = request.user
   r = houserentconfir.objects.get(id=id)
   return render(request,'user/rentedview.html', locals())

@login_required
def buyview(request,id):
   user = request.user
   p = housebuy.objects.get(id=id)
   if request.method == 'POST':
    a_id = request.POST.get('a_id')
    amount = request.POST.get('amount')

    edi = housebuy.objects.get(id=a_id)
    edi.status = 'sold'
    edi.amount = amount
    edi.save()
    messages.success(request,'house is sold successfully waiting for buyer')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   return render(request,'user/buyview.html', locals())

@login_required
def profilepage(request):
   return render(request,'user/profile.html', locals())

@login_required
def transfer(request):
   user = request.user
   if request.method == 'POST':
      amount =request.POST.get('amount')
      walletID =request.POST.get('walletID')
      ba = userwallet.objects.get(user=user)
      if float(amount) > ba.amount:
         messages.error(request,'insuficiant funds')
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      else:
         try:
            uw = userwallet.objects.get(id=walletID)
            uw.amount += float(amount)
            uw.save()

            
            ba = userwallet.objects.get(user=user)
            ba.amount -= float(amount)
            ba.save()
            bn = ba.user.username
            tc = trans_his.objects.create(user=request.user,name=bn,amount=amount)
            tc.save()
            messages.success(request,'Transfer is successful')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         except userwallet.DoesNotExist:
            messages.error(request, "Wallet ID mismatch: No wallet found with the provided ID.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         
   else:
    return render(request,'user/transfer.html', locals())

@login_required
def transf_his(request):
   x = trans_his.objects.filter(user=request.user)
   return render(request,'user/transf_his.html', locals())

@login_required
def withdraw(request):
  x = paymentmethod.objects.all()
  return render(request,'user/withdraw.html', locals())

@login_required
def withdrawam(request, id):
   x = paymentmethod.objects.get(id=id)
   return render(request,'user/withdrawam.html', locals())


@login_required
def withdrawconf(request):
   user=request.user
   p_id = request.GET.get('p_id')
   amount = request.GET.get('amount')
   x = paymentmethod.objects.get(pk=p_id)
  

   if request.method == 'POST':
      proof =  request.FILES.get('proof')
      address = request.POST.get('address')

      dc = withdraw_his.objects.create(user=request.user,paymentm=x,amount=amount,address=address,)
   
      messages.success(request,'you have made a withdraw')
      return redirect('/user')
   else:
    return render(request,'user/withdrawconf.html', locals())


@login_required
def withdrawhis(request):
   x = withdraw_his.objects.filter(user=request.user)
   return render(request,'user/withdrawhis.html', locals())


@login_required
def shares_view(request):
   user = request.user
   x = Shares.objects.all()
   amount = request.POST.get('amount')
   a_id = request.POST.get('a_id')
   if request.method == 'POST':
      ba = userwallet.objects.get(user=user)
      if float(amount) > ba.amount:
         messages.error(request,'insuficiant funds')
         return redirect('/assets')
      else:
         ba = userwallet.objects.get(user=request.user)
         ba.amount -= float(amount)
         print(ba.amount,'new balance')
         ba.save()
         shares_id = Shares.objects.get(id=a_id)
         u_s = user_Shares.objects.create(
            user = user,shares=shares_id,name=shares_id.name,amount=amount,value=amount,interest_rate=shares_id.interest_rate,update_interval=shares_id.update_interval,end_interval=shares_id.end_interval
         )
         
         messages.success(request,'shares is bought successfully')
         return redirect('/myshares')
   else:
    return render(request,'user/shares.html',{'x':x})


@login_required
def myshares(request):
   user = request.user
   try:
     ms = user_Shares.objects.filter(user=request.user)
   except:
      ms = user_Shares.DoesNotExist
      ms = None
   return render(request,'user/myshares.html',locals())



def newslet(request):
   email = request.POST.get('email')
   if request.method == 'POST':
      x = newsletter.objects.get_or_create(email=email)
      messages.success(request,'Email added successfully')
      return redirect('/')
   else:
    return render(request,'home/newslet.html')









def about(request):
    return render(request,'home/about.html')

def blogs(request):
    return render(request,'home/blogs.html')

def faq(request):
    return render(request,'home/faq.html')

def contact(request):
    return render(request,'home/contact.html')