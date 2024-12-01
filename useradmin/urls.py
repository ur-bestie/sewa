from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('houseview',views.houseview, name='houseview'),
    path('houseadd',views.houseadd, name='houseadd'),
    path('userdeposit',views.userdeposit, name='userdeposit'),
    path('userappr/<str:id>',views.userappr, name='userappr'),
    path('userrejec/<str:id>',views.userrejec, name='userrejec'),
    path('userbalance',views.userbalance, name='userbalance'),
    path('add/<str:id>',views.add, name='add'),
    
    ]