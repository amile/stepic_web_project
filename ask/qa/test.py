from django import forms

class Answer(object):
	"""docstring for AskForm"""
	
	def __init__(self, *args, **kwargs):
		
		text = kwargs.get('text')

class AnswerForm(Answer):
	"""docstring for AskForm"""

	text = forms.CharField(widget=forms.Textarea)
	
	def __init__(self, *args, **kwargs):
		print args, kwargs
		super(AnswerForm, self).__init__(*args, **kwargs)
		self.question = args[0]

	def save(self):
		users = User.objects.all()[:]
		user = random.choice(users)
		self.cleaned_data['author'] = user
		self.cleaned_data['question'] = self.question
		answer = Answer(**self.cleaned_data)
		answer.save()
		return answer

def test():
	question = 'Question'
	form = AnswerForm()
	return form

def test1(*args, **kwargs):
	# text = kwargs.get('text')
	text = args[0]
	print text

test()
