from django.conf.urls.defaults import *

urlpatterns = patterns('gesta.nic.views',
#     (r'^$', 'index'),
     (r'^$', 'index'),
     (r'check/$', 'Check'),
     (r'mod/$', 'ModificarDominio'),
)
