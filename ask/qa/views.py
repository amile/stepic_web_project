# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage
from qa.models import Question, Answer
from django.core.urlresolvers import reverse

def test(request, *args, **kwargs):
	return HttpResponse('OK')

def question(request, *args, **kwargs):
	question = get_object_or_404(Question, id=kwargs['id'])
	answers = 0
	return render(request, 'question.html', {'question': question, 'answers': answers})

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
