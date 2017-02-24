from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, date, time
from .models import *
import bcrypt
# Create your views here.
def index(request):
	return render(request, 'main/index.html')

def login_user(request):
	login = User.objects.login_user(request,request.POST)
	if login[0]:
		request.session['user_id'] = login[1].id
		return redirect('/home')
	return redirect('/')

def success(request):
	context = {
		'users': User.objects.all(),
		"curr_user": User.objects.get(id=request.session['user_id'])
	}
	return render(request, 'main/success.html', context)

def home(request):
	today = date.today()
	time = datetime.now().time
	user = User.objects.filter(id=request.session['user_id'])
	context = {
		"curr_user": User.objects.get(id=request.session['user_id']),
		"today": today,
		"curr_time":time,
		"today_appointments": Appointment.objects.filter(date=today).order_by("time"),
		"future_appointments": Appointment.objects.exclude(date=today),
	}
	return render(request, 'main/home.html', context)


def create_user(request):
	if User.objects.validate(request,request.POST) == True:
		user = User.objects.create(
			first_name = request.POST.get('first_name'),
			last_name = request.POST.get('last_name'),
			email = request.POST.get('email'),
			password = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())
		)
		request.session['user_id'] = user.id
		return redirect('/success')
	return redirect('/')

def appointments(request):
	Appointment.objects.create(
		date = str(request.POST.get('date')),
		time = request.POST.get('time'),
		task = request.POST.get('task'),
		user = User.objects.get(id=request.session["user_id"])
	)
	return redirect('/home')



def editpage(request, id):
    context = {
        "appointment": Appointment.objects.get(id=id),
		'users': User.objects.all(),
		"curr_user": User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'main/edit.html', context)

def edit(request):
	appointment = Appointment.objects.get(id=id),
	Appointment.objects.filter(appointment=appointment).update(
		user = User.objects.get(id=request.session["user_id"]),
		date = str(request.POST.get('date')),
		time = request.POST.get('time'),
		task = request.POST.get('task'),
	)
	return redirect ('/home')

def delete(request, id):
    Appointment.objects.filter(id=id).delete()
    return redirect ('/home')
