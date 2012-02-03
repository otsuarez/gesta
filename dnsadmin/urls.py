from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^dns/$', 'gesta.dnsadmin.views.index'),
# ----------------------------------------------------------------------------- #
#	zone stuff
# ----------------------------------------------------------------------------- #
     (r'^dns/zone/add/$', 'gesta.dnsadmin.views.zone_add'),
     (r'^dns/zone/del/(?P<zid>\d+)/$', 'gesta.dnsadmin.views.zone_del'),
     (r'^dns/zone/edit/(?P<zid>\d+)/$', 'gesta.dnsadmin.views.zone_edit'),     
# ----------------------------------------------------------------------------- #
#	records stuff
# ----------------------------------------------------------------------------- #
     (r'^dns/zone/(?P<zid>\d+)/rr/add/$', 'gesta.dnsadmin.views.record_add'),
     (r'^dns/zone/list/(?P<zid>\d+)/$', 'gesta.dnsadmin.views.zone_list'),     
     (r'^dns/rr/del/(?P<id>\d+)/$', 'gesta.dnsadmin.views.record_del'),
# ----------------------------------------------------------------------------- #
     (r'^dns/logout', 'gesta.dnsadmin.views.logout_view'),
     (r'^logout', 'gesta.dnsadmin.views.logout_view'),
     (r'^dns/accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
     (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^dns/admin/', include('django.contrib.admin.urls')),
)
