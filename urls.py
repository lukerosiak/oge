from django.conf.urls.defaults import *


urlpatterns = patterns('',
    
	(r'^$', 'quarterback.oge.views.index'), 
	(r'^(?P<id>\d+)/$', 'quarterback.oge.views.text'), 

)

