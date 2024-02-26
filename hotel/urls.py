from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('room/<str:pk>/',views.room,name='room'),
    path("register/",views.createroom,name='croom'),
    path('profile/<str:pk>',views.profileview,name='profile'),
    path("update/<str:pk>",views.updateroom,name='uroom'),
    path("delete/<str:pk>",views.deleteroom,name='droom'),
    path('login/',views.loginpage,name='loginp'),
    path('logout/',views.logoutpage,name='logoutp'),
    path('registerp/',views.registerpage,name='registerp'),
    path("deletemsg/<str:pk>",views.deletemsg,name='deletem'),
]
