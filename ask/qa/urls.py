from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.new, name='new'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^question/(?P<id>[0-9]+)/$', views.question, name='question'),
    url(r'^ask/$', views.add_question, name='add_question'),
    url(r'^popular/$', views.popular, name='popular'),
    url(r'^new/$', views.test, name='new'),
]