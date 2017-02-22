from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import bcrypt
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate(self, request, post):
        criteria = True
        if len(post.get('email')) < 1:
            criteria = False
            messages.add_message(request, messages.INFO, "Your email must have characters!")
        if not EMAIL_REGEX.match(post.get('email')):
            criteria = False
            messages.add_message(request, messages.INFO, "This email is not a valid email address!")
        if len(post.get('first_name')) < 3 or len(post.get('last_name')) < 3:
            criteria = False
            messages.add_message(request, messages.INFO, "First name and last name must be longer than 2 characters.")
        if len(post.get('password')) < 8:
            criteria = False
            messages.add_message(request, messages.INFO, "Password must be at least 8 characters long!")
        if len(post.get('password')) < 1:
            criteria = False
            messages.add_message(request, messages.INFO, "Password must have at least 1 character!")
        if post.get('password') != post.get('password_confirm'):
            criteria = False
            messages.add_message(request, messages.INFO, "Your passwords do not match!")
        return(criteria)

    def login_user(self,request, post):
        user = self.filter(email=post.get('email')).first()
        if user and bcrypt.hashpw(post.get('password').encode(), user.password.encode()) == user.password:
            return (True, user)
        messages.add_message(request, messages.INFO, "Your email and password do not match!")
        return (False, 'notuser')

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
