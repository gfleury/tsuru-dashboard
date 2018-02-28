from django.conf.urls import include, url

import instance.views as views


urlpatterns = [
    url(r'^instance/$', views.list, name='autoscale-instance-list'),
    url(r'^datasource/', include('tsuru_dashboard.autoscale.datasource.urls')),
    url(r'^alarm/', include('tsuru_dashboard.autoscale.alarm.urls')),
    url(r'^action/', include('tsuru_dashboard.autoscale.action.urls')),
    url(r'^instance/', include('tsuru_dashboard.autoscale.instance.urls')),
    url(r'^wizard/', include('tsuru_dashboard.autoscale.wizard.urls')),
]
