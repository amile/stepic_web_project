
from django import forms

from django.contrib.auth.models import User
from qa.models import Question, Answer
import random

class AskForm(forms.Form):
	"""docstring for AskForm"""
	title = forms.CharField()
	text = forms.CharField(widget=forms.Textarea)

	def save(self):
		users = User.objects.all()[:]
		user = random.choice(users)
		self.cleaned_data['author'] = user
		question = Question(**self.cleaned_data)
		question.save()
		return question

class AnswerForm(forms.Form):
	"""docstring for AskForm"""

	text = forms.CharField(widget=forms.Textarea)
	question = forms.IntegerField()
	
	def __init__(self, question, *args, **kwargs):
		print question, args, kwargs
		super(AnswerForm, self).__init__(*args, **kwargs)
		self._question = question

	def save(self):
		users = User.objects.all()[:]
		user = random.choice(users)
		self.cleaned_data['author'] = user
		self.cleaned_data['question'] = self._question
		answer = Answer(**self.cleaned_data)
		answer.save()
		return answer

		
