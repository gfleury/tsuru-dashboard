from django.conf.urls import url

from tsuru_dashboard.autoscale.instance import views


urlpatterns = [
    url(r'^(?P<name>[\w-]+)/$', views.get, name='instance-get'),
]
