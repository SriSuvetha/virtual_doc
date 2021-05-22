"""HospitalManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sitehandler.views import *
from sitehandler import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name='homepage'),
    path('login/',loginpage,name='loginpage'),
    path('login/patienthome.html',views.dashboard),
    path('createaccount',createaccountpage,name='createaccountpage'),
    path('admin_login/',Login_admin,name='login_admin'),
    path('adminhome/',AdminHome,name='adminhome'),
    path('adminlogout/',Logout_admin,name='adminlogout'),
    path('adminaddDoctor/',adminaddDoctor,name='adminaddDoctor'),
    path('home/',Home,name='home'),
    path('makeappointments/',MakeAppointments,name='makeappointments'),
    path('viewappointments/',viewappointments,name='viewappointments'),
    path('PatientDeleteAppointment<int:pid>',patient_delete_appointment,name='patient_delete_appointment'),
    path('logout/',Logout,name='logout'),
]

