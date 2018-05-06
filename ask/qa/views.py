# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import string 
import random
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage
from qa.models import Question, Answer, Session
from django.contrib.auth.models import User
from qa.forms import AskForm, AnswerForm, SignupForm, LoginForm
from django.core.urlresolvers import reverse


def create_random_string():
	choice = string.ascii_lowercase + string.ascii_uppercase + string.digits
	s = ''
	while len(s) < 20:
		i = random.choice(choice)
		if i not in s:
		    s += i
	return s

def create_session(user):
	session = Session()
	session.key = create_random_string()
	session.user = user
	session.expires = datetime.now() + timedelta(days=5)
	session.save()
	return session.key

def do_login(login, password):
	try:
		user = User.objects.get(username=login)
	except User.DoesNotExist:
		return None
	if (user.password != password):
		return None
	return create_session(user)

def test(request, *args, **kwargs):
	return HttpResponse('OK')

def question(request, *args, **kwargs):
	question = get_object_or_404(Question, id=kwargs['id'])
	url = question.get_absolute_url()
	user = request.user
	if request.method == 'POST':

		form = AnswerForm(user, question, request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(url)

	else:

		form = AnswerForm(user, question)
	
	return render(request, 'question.html', {'question': question, 
											'form': form, })

def add_question(request, *args, **kwargs):
	user = request.user
	if request.method == 'POST':
		form = AskForm(user, request.POST)
		if form.is_valid():
			question = form.save()
			url = question.get_absolute_url()
			return HttpResponseRedirect(url)
	else:
		form = AskForm(user)
	return render(request, 'ask.html', {'form': form,})

def new(request, *args, **kwargs):
	sessionid = request.COOKIES.get('sessionid', 'no session')
	user = request.user
	try:
		page = int(request.GET.get('page', 1))
	except ValueError:
		raise Http404
	questions = Question.objects.new()
	paginator = Paginator(questions, 10)
	try:
		page = paginator.page(page)
	except EmptyPage: 
		page = paginator.page(paginator.num_pages)
	return render(request, 'main.html', 
		{'questions': questions, 
		'paginator': paginator,
		'page': page, 'sessionid': sessionid, 'user': user.id,})

def popular(request, *args, **kwarg):
	try:
		page = int(request.GET.get('page', 1))
	except ValueError:
		raise Http404
	questions = Question.objects.popular()
	paginator = Paginator(questions, 10)
	try:
		page = paginator.page(page)
	except EmptyPage: 
		page = paginator.page(paginator.num_pages)
	return render(request, 'popular.html', 
		{'questions': questions, 
		'paginator': paginator,
		'page': page,})

def signup(request, *args, **kwargs):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			sessionid = create_session(user)
			url = request.POST.get('continue', '/')
			response = HttpResponseRedirect(url)
			response.set_cookie('sessionid', sessionid)
			return response
	else:
		form = SignupForm()
	return render(request, 'signup.html', {'form': form,})

def login(request, *args, **kwargs):
	if request.method == 'POST':
		login = request.POST.get('username')
		password = request.POST.get('password')
		sessionid = do_login(login, password)
		if sessionid:
			response = HttpResponseRedirect('/')
			response.set_cookie('sessionid', sessionid,)
			return response
		else:
			error = 'Wrong login/password'
	error = None
	form = LoginForm()
	return render(request, 'login.html', {'form': form, 'error': error})

