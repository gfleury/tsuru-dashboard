from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from tsuru_dashboard.autoscale.action.forms import ActionForm
from tsuru_dashboard.autoscale.action import client


def new(request):
    form = ActionForm(request.POST or None)

    if form.is_valid():
        token = request.session.get("tsuru_token").split(" ")[-1]
        client.new(form.cleaned_data, token)
        messages.success(request, u"Action saved.")
        url = "{}".format(reverse('action-list'))
        return redirect(url)

    context = {"form": form}
    return render(request, "autoscale/action/new.html", context)


def list(request):
    token = request.session.get("tsuru_token").split(" ")[-1]
    actions = client.list(token).json()
    context = {
        "list": actions,
    }
    return render(request, "autoscale/action/list.html", context)


def get(request, name):
    token = request.session.get("tsuru_token").split(" ")[-1]
    action = client.get(name, token).json()
    context = {
        "item": action,
    }
    return render(request, "autoscale/action/get.html", context)


def remove(request, name):
    token = request.session.get("tsuru_token").split(" ")[-1]
    client.remove(name, token)
    messages.success(request, u"Action {} removed.".format(name))
    url = "{}".format(reverse('action-list'))
    return redirect(url)
