from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

def dashboard(request):
	return render(request,'patienthome.html')

def homepage(request):
	return render(request,'index.html')

def Login_admin(request):
	error = ""
	if request.method == 'POST':
		u = request.POST['username']
		p = request.POST['password']
		user = authenticate(username=u,password=p)
		try:
			if user.is_staff:
				login(request,user)
				error = "no"
				
			else:
				error = "yes"

		except:
			error = "yes"
	d = {'error' : error}
	return render(request,'adminlogin.html',d)

def loginpage(request):
	error = ""
	if request.method == 'POST':
		u = request.POST['email']
		p = request.POST['password']
		csrfContext = RequestContext(request)
		user = authenticate(csrfContext,username=u,password=p)
		print(user)
		if user is not None:
			login(request,user)
			g = request.user.groups.all()[0].name
			print(g)
			if g == 'Doctor':
				return render(request,'doctorhome.html')
			elif g == 'Patient':
				return render(request,'patienthome.html')
			elif g == 'Admin':
				return render(request,'adminhome.html')
			
			
	return render(request,'login.html')

def createaccountpage(request):
	error = ""
	user="none"
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['password']
		repeatpassword = request.POST['repeatpassword']
		gender = request.POST['gender']
		phonenumber = request.POST['phonenumber']
		address = request.POST['address']
		birthdate = request.POST['dateofbirth']
		bloodgroup = request.POST['bloodgroup']
		try:
			if password == repeatpassword:
				Patient.objects.create(name=name,email=email,password=password,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup)
				user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
				pat_group = Group.objects.get(name='Patient')
				pat_group.user_set.add(user)
				user.save()
				error = "no"
			else:
				error = "yes"
		except Exception as e:
			error = "yes"
	d = {'error' : error}

	return render(request,'createaccount.html',d)


def adminaddDoctor(request):
	error = ""
	user="none"
	if not request.user.is_staff:
		return redirect('login_admin')

	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['password']
		repeatpassword =  request.POST['repeatpasssword']
		gender = request.POST['gender']
		phonenumber = request.POST['phonenumber']
		address = request.POST['address']
		birthdate = request.POST['dateofbirth']
		bloodgroup = request.POST['bloodgroup']
		specialization = request.POST['specialization']
		
		try:
			if password == repeatpassword:
				Doctor.objects.create(name=name,email=email,password=password,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup,specialization=specialization)
				user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
				doc_group = Group.objects.get(name='Doctor')
				doc_group.user_set.add(user)
				user.save()
				error = "no"
			else:
				error = "yes"
		except Exception as e:
			error = "yes"
	d = {'error' : error}
	return render(request,'adminadddoctor.html',d)


def patient_delete_appointment(request,pid):
	if not request.user.is_active:
		return redirect('loginpage')
	appointment = Appointment.objects.get(id=pid)
	appointment.delete()
	return redirect('viewappointments')


def Logout(request):
	if not request.user.is_active:
		return redirect('loginpage')
	logout(request)
	return redirect('homepage')

def Logout_admin(request):
	if not request.user.is_staff:
		return redirect('login_admin')
	logout(request)
	return redirect('homepage')

def AdminHome(request):
	
	if not request.user.is_staff:
		return redirect('login_admin')
	return render(request,'adminhome.html')

def Home(request):
	if not request.user.is_active:
		return redirect('loginpage')

	g = request.user.groups.all()[0].name
	if g == 'Doctor':
		return render(request,'doctorhome.html')
	
	elif g == 'Patient':
		return render(request,'patienthome.html')




def MakeAppointments(request):
	error = ""
	if not request.user.is_active:
		return redirect('loginpage')
	alldoctors = Doctor.objects.all()
	d = { 'alldoctors' : alldoctors }
	g = request.user.groups.all()[0].name
	if g == 'Patient':
		if request.method == 'POST':
			doctoremail = request.POST['doctoremail']
			doctorname = request.POST['doctorname']
			patientname = request.POST['patientname']
			patientemail = request.POST['patientemail']
			appointmentdate = request.POST['appointmentdate']
			appointmenttime = request.POST['appointmenttime']
			symptoms = request.POST['symptoms']
			try:
				Appointment.objects.create(doctorname=doctorname,doctoremail=doctoremail,patientname=patientname,patientemail=patientemail,appointmentdate=appointmentdate,appointmenttime=appointmenttime,symptoms=symptoms,status=True,prescription="")
				error = "no"
			except:
				error = "yes"
			e = {"error":error}
			return render(request,'pateintmakeappointments.html',e)
		elif request.method == 'GET':
			return render(request,'pateintmakeappointments.html',d)

def viewappointments(request):
	if not request.user.is_active:
		return redirect('loginpage')

	g = request.user.groups.all()[0].name
	if g == 'Patient':
		upcomming_appointments = Appointment.objects.filter(patientemail=request.user,appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
		
		previous_appointments = Appointment.objects.filter(patientemail=request.user,appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(patientemail=request.user,status=False).order_by('-appointmentdate')
		
		d = { "upcomming_appointments" : upcomming_appointments, "previous_appointments" : previous_appointments }
		return render(request,'patientviewappointments.html',d)
	elif g == 'Doctor':
		if request.method == 'POST':
			prescriptiondata = request.POST['prescription']
			idvalue = request.POST['idofappointment']
			Appointment.objects.filter(id=idvalue).update(prescription=prescriptiondata,status=False)
			
		upcomming_appointments = Appointment.objects.filter(doctoremail=request.user,appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
		
		
		
		d = { "upcomming_appointments" : upcomming_appointments }
		return render(request,'doctorviewappointment.html',d)
	
