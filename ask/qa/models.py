# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, connection
from django.contrib.auth.models import User
from django.utils import timezone

class QuestionManager(models.Manager):
	"""docstring for QuestionManager"""

	def new(self):
		cursor = connection.cursor()
		cursor.execute("""
			SELECT title FROM qa_question ORDER BY added_at DESC
			LIMIT 10
		""")
		return cursor.fetchall()

	def popular(self):
		cursor = connection.cursor()
		cursor.execute("""
			SELECT qa_question.* from qa_question, 
				(SELECT question_id, count(*) as likes 
				FROM qa_question_likes 
				GROUP BY question_id 
				ORDER BY likes DESC) as t1
			where qa_question.id = t1.question_id
		""")
		return cursor.fetchall()


class Question(models.Model):
	"""docstring for Question"""
	title = models.CharField(max_length=200)
	text = models.TextField()
	added_at = models.DateField(blank=True, auto_now_add=True)
	rating = models.IntegerField(default=0)
	author = models.ForeignKey(User)
	likes = models.ManyToManyField(User, related_name='likes')
	objects = QuestionManager()

		
class Answer(models.Model):
	"""docstring for Question"""
	text = models.TextField()
	added_at = models.DateField(blank=True, auto_now_add=True)
	rating = models.IntegerField(default=0)
	question = models.OneToOneField(Question)
	author = models.ForeignKey(User)
