# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, connection
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse

class QuestionManager(models.Manager):
	"""docstring for QuestionManager"""

	def new(self):
		# cursor = connection.cursor()
		# cursor.execute("""
		# 	SELECT title FROM qa_question ORDER BY added_at DESC
		# 	LIMIT 10
		# """)
		# return cursor.fetchall()
		return self.order_by('-id')

	def popular(self):
		# cursor = connection.cursor()
		# cursor.execute("""
		# 	SELECT qa_question.* from qa_question, 
		# 		(SELECT question_id, count(*) as likes 
		# 		FROM qa_question_likes 
		# 		GROUP BY question_id 
		# 		ORDER BY likes DESC) as t1
		# 	where qa_question.id = t1.question_id
		# """)
		# return cursor.fetchall()
		popular_list = self.all()[:]
		sort = sorted(popular_list, key=lambda question: question.likes.count(), reverse=True)

		return self.order_by('-rating')


class Question(models.Model):
	"""docstring for Question"""
	title = models.CharField(max_length=200)
	text = models.TextField()
	added_at = models.DateField(blank=True, auto_now_add=True)
	rating = models.IntegerField(default=0)
	author = models.ForeignKey(User)
	likes = models.ManyToManyField(User, related_name='likes')
	objects = QuestionManager()

	def get_answers(self):
		return self.answer_set.all()
		
	def get_absolute_url(self):
		return reverse('question', args=[str(self.id)])

		
class Answer(models.Model):
	"""docstring for Question"""
	text = models.TextField()
	added_at = models.DateField(blank=True, auto_now_add=True)
	rating = models.IntegerField(default=0)
	question = models.ForeignKey(Question)
	author = models.ForeignKey(User)
