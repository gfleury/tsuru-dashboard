from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from tsuru_dashboard.autoscale.datasource.forms import DataSourceForm
from tsuru_dashboard.autoscale.datasource import client


def new(request):
    form = DataSourceForm(request.POST or None)

    if form.is_valid():
        token = request.session.get("tsuru_token").split(" ")[-1]
        response = client.new(form.cleaned_data, token)
        if response.status_code > 399:
            messages.error(request, response.text)
        else:
            messages.success(request, u"Data source saved.")
        url = "{}".format(reverse('datasource-list'))
        return redirect(url)

    context = {"form": form}
    return render(request, "autoscale/datasource/new.html", context)


def list(request):
    token = request.session.get("tsuru_token").split(" ")[-1]
    datasources = client.list(token).json()
    context = {
        "list": datasources,
    }
    return render(request, "autoscale/datasource/list.html", context)


def remove(request, name):
    token = request.session.get("tsuru_token").split(" ")[-1]
    client.remove(name, token)
    messages.success(request, u"Data source  {} remove.".format(name))
    url = "{}".format(reverse('datasource-list'))
    return redirect(url)


def get(request, name):
    token = request.session.get("tsuru_token").split(" ")[-1]
    datasource = client.get(name, token).json()
    context = {
        "item": datasource,
    }
    return render(request, "autoscale/datasource/get.html", context)
