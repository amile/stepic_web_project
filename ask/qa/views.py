# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage
from qa.models import Question, Answer
from qa.forms import AskForm, AnswerForm
from django.core.urlresolvers import reverse

def test(request, *args, **kwargs):
	return HttpResponse('OK')

def question(request, *args, **kwargs):
	question = get_object_or_404(Question, id=kwargs['id'])
	url = question.get_absolute_url()
	if request.method == 'POST':
		form = AnswerForm(question, request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect(url)
	else:
		form = AnswerForm(question)
	
	return render(request, 'question.html', {'question': question, 
											'form': form, })

def add_question(request, *args, **kwargs):
	if request.method == 'POST':
		form = AskForm(request.POST)
		if form.is_valid():
			question = form.save()
			url = question.get_absolute_url()
			return HttpResponseRedirect(url)
	else:
		form = AskForm()
	return render(request, 'ask.html', {'form': form,})

def new(request, *args, **kwargs):
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
		'page': page,})

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
