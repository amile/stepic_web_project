from django.utils.deprecation import MiddlewareMixin
from qa.models import Question, Answer, Session
from datetime import datetime


class CheckSessionMiddleware(MiddlewareMixin):
	"""docstring for CheckSessionMiddleware"""

	def process_request(self, request):
		try:
			sessid = request.COOKIES.get('sessionid')
			session = Session.objects.get(key=sessid, expires__gt=datetime.now(),)
			request.session = session
			request.user = session.user
		except Session.DoesNotExist:
			request.session = None
			request.user = None
		