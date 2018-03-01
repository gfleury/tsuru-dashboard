from django.shortcuts import render

from tsuru_dashboard.autoscale.event import client


def list(request, alarm_name):
    token = request.session.get("tsuru_token").split(" ")[-1]
    events = client.list(alarm_name, token).json()
    context = {
        "list": events,
    }
    return render(request, "event/list.html", context)
