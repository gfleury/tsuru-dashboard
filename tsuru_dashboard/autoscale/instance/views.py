from django.shortcuts import render

import client
from tsuru_dashboard.autoscale.event import client as eclient


def list(request, app_name=None):
    token = request.session.get('tsuru_token').split(" ")[-1]
    instances = client.list(token).json()
    context = {
        "list": instances,
    }
    return render(request, "autoscale/instance/list.html", context)


def get(request, name):
    token = request.session.get('tsuru_token').split(" ")[-1]
    instance = client.get(name, token).json()
    alarms = client.alarms_by_instance(name, token).json() or []

    events = []

    for alarm in alarms:
        events.extend(eclient.list(alarm["name"], token).json() or [])

    context = {
        "item": instance,
        "alarms": alarms,
        "events": events,
    }
    return render(request, "autoscale/instance/get.html", context)
