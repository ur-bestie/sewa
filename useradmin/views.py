from django.shortcuts import render, redirect
from userapp.models import *
from .forms import HouseForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def index(request):
    return render(request,'useradmin/index.html')




def houseview(request):
    x = House.objects.all()
    return render(request,'useradmin/houseview.html', locals())

def houseadd(request):
    form = HouseForm()  # Initialize the form at the start, so it exists for both GET and POST

    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES)
        files = request.FILES.getlist('other_pictures')  # Get the list of uploaded files

        if form.is_valid():
            house = form.save()  # Save the house object

            # Loop over each uploaded file and create a HousePicture instance
            for file in files:
                picture = HousePicture.objects.create(image=file)
                house.other_pictures.add(picture)  # Associate each picture with the house

            house.save()  # Save the house after adding the pictures
            return redirect('/useradmin/houseview')

    return render(request, 'useradmin/houseadd.html', {'form': form})
    


def userdeposit(request):
    x = deposit_his.objects.all()
    return render(request,'useradmin/userdeposit.html', locals())


def userappr(request, id):
    x = deposit_his.objects.get(id=id)
    x.status = True
    ba = userwallet.objects.get(user=x.user)
    ba.amount += float(x.amount)
    ba.save()
    x.save()
    messages.success(request,'deposit approved')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def userrejec(request, id):
    x = deposit_his.objects.get(id=id)
    x.status = False
    nt = notification.objects.get_or_create(user=x.user,subject='Rejected Deposit',message='you made a fake deposit of {{x.amount}}')
    messages.success(request,'Deposit is rejected Successfully')
    x.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def userbalance(request):
 x = userwallet.objects.all()
 return render(request,'useradmin/userbalance.html', locals())


def add(request, id):
    x = userwallet.objects.get(id=id)
    if request.method == 'POST':
        amount = request.POST.get(amount)
        x.amount += float(amount)
        x.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
     return render(request,'useradmin/userbalance.html', locals())


