
from django import forms

from django.contrib.auth.models import User
from qa.models import Question, Answer
import random

class AskForm(forms.Form):
	"""docstring for AskForm"""
	title = forms.CharField()
	text = forms.CharField(widget=forms.Textarea)

	def __init__(self, user, *args, **kwargs):
		self._user = user
		super(AnswerForm, self).__init__(*args, **kwargs)

	def save(self):
		self.cleaned_data['author'] = self._user
		question = Question(**self.cleaned_data)
		question.save()
		return question

class AnswerForm(forms.Form):
	"""docstring for AnswerForm"""

	text = forms.CharField(widget=forms.Textarea)
	question = forms.IntegerField(widget=forms.HiddenInput(), required=False)
	
	def __init__(self, user, question, *args, **kwargs):
		self._user = user
		self._question = question
		super(AnswerForm, self).__init__(*args, **kwargs)
		

	def save(self):
		self.cleaned_data['author'] = self._user
		self.cleaned_data['question'] = self._question
		answer = Answer(**self.cleaned_data)
		answer.save()
		return answer

class SignupForm(forms.Form):
	"""docstring for SignupForm"""
	username = forms.CharField()
	email = forms.EmailField(required=False)
	password = forms.CharField(widget=forms.PasswordInput())

	def save(self):
		user = User(**self.cleaned_data)
		user.save()
		return user

class LoginForm(forms.Form):
	"""docstring for LoginForm"""
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())

	

		
