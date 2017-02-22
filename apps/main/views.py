from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
# Create your views here.
def index(request):
	return render(request, 'main/index.html')

def success(request):
	context = {
		'users': User.objects.all(),
		"curr_user": User.objects.get(id=request.session['user_id'])
	}
	return render(request, 'main/success.html', context)

def home(request):
	context = {
		'users': User.objects.all(),
		"curr_user": User.objects.get(id=request.session['user_id'])
	}
	return render(request, 'main/home.html', context)

def login_user(request):
	login = User.objects.login_user(request,request.POST)
	if login[0]:
		request.session['user_id'] = login[1].id
		return redirect('/home')
	return redirect('/')


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
