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
    path('housebuy/<str:id>',views.housebuy, name='housebuy'),
    path('profilepage',views.profilepage, name='profilepage'),




    path('login',views.login, name='login'),
    path('register',views.register, name='register'),
    path('logout',views.logout, name='logout'),
    path('register',views.register, name='register'),
    path('about',views.about, name='about'),
    path('blogs',views.blogs, name='blogs'),
    path('faq',views.faq, name='faq'),
    path('contact',views.contact, name='contact'),
    
    ]