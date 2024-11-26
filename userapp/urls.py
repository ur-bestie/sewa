from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('user',views.user, name='user'),
    path('deposit',views.deposit, name='deposit'),
    path('depositam/<str:id>',views.depositam, name='depositam'),
    path('depositconf',views.depositconf, name='depositconf'),
    path('deposithis',views.deposithis, name='deposithis'),
    path('assets',views.assets, name='assets'),
    path('myassets',views.myassets, name='myassets'),
    path('housepurchase',views.housepurchase, name='housepurchase'),
    path('housedetails/<str:id>',views.housedetails, name='housedetails'),
    path('housebuy/<str:id>',views.housebuy_view, name='housebuy'),
    path('profilepage',views.profilepage, name='profilepage'),
    path('house_cert/<str:id>',views.house_cert, name='house_cert'),
    path('properties',views.properties, name='properties'),
    path('houserent',views.houserentview, name='houserent'),
    path('houserentinfo/<str:id>',views.houserentinfo, name='houserentinfo'),
    path('houserentpay/<str:id>',views.houserentpay, name='houserentpay'),
    path('rentedview/<str:id>',views.rentedview, name='rentedview'),
    path('buyview/<str:id>',views.buyview, name='buyview'),
    path('transfer',views.transfer, name='transfer'),
    path('withdraw',views.withdraw, name='withdraw'),
    path('withdrawam/<str:id>',views.withdrawam, name='withdrawam'),
    path('withdrawconf',views.withdrawconf, name='withdrawconf'),
    path('withdrawhis',views.withdrawhis, name='withdrawhis'),
    path('transf_his',views.transf_his, name='transf_his'),
    path('newslet',views.newslet, name='newslet'),





    path('login',views.login, name='login'),
    path('register',views.register, name='register'),
    path('logout',views.logout, name='logout'),
    path('register',views.register, name='register'),
    path('about',views.about, name='about'),
    path('blogs',views.blogs, name='blogs'),
    path('faq',views.faq, name='faq'),
    path('contact',views.contact, name='contact'),
    
    ]