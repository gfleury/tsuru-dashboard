import requests

from datetime import datetime, timedelta
from time import mktime

from tsuru_dashboard.metrics.backends import base


class Prometheus(object):
    def __init__(self, url, query, date_range=None):
        self.url = url
        self.query = query
        self.date_range = date_range

    @property
    def delta(self):
        if not self.date_range:
            return {"hours": 1}

        if "h" in self.date_range:
            return {"hours": int(self.date_range.replace("h", ""))}

        if "d" in self.date_range:
            return {"days": int(self.date_range.replace("d", ""))}

        if "w" in self.date_range:
            return {"days": int(self.date_range.replace("w", "")) * 7}

    @property
    def start(self):
        return self.end - timedelta(**self.delta)

    @property
    def end(self):
        return datetime.now()

    @property
    def resolution(self):
        return (self.end - self.start).total_seconds() / 250

    def default_processor(self, results):
        def toMs(x):
            if len(x) == 2:
                return [x[0] * 1000, x[1]]
            return x

        return list(map(toMs, results))

    def get_metrics(self, query, processor=None):
        url = self.url
        url += "/api/v1/query_range?"
        url += query
        url += "start={}".format(mktime(self.start.timetuple()))
        url += "&end={}".format(mktime(self.end.timetuple()))
        url += "&step={}".format(self.resolution)
        result = requests.get(url, verify=False)

        if processor is None:
            result = result.json()['data']['result'][0]['values']
            processor = self.default_processor

        return processor(result)

    def mem_max(self, interval=None):
        data = {"min": 0, "max": 1024}
        query = "query=avg(container_memory_usage_bytes{pod_name=~\"%s.*\", container_name!=\"POD\"})/1024/1024&" % self.query
        data["avg"] = self.get_metrics(query)

        query = "query=max(container_memory_usage_bytes{pod_name=~\"%s.*\", container_name!=\"POD\"})/1024/1024&" % self.query
        data["max"] = self.get_metrics(query)

        query = "query=min(container_memory_usage_bytes{pod_name=~\"%s.*\", container_name!=\"POD\"})/1024/1024&" % self.query
        data["min"] = self.get_metrics(query)
        return {"data": data}

    def cpu_max(self, interval=None):
        data = {"min": 0, "max": 100}
        query = "query=avg(sum(rate(container_cpu_usage_seconds_total{pod_name=~\"%s.*\", container_name!=\"POD\"}[2m])) by (name)) * 100&" % self.query
        data["avg"] = self.get_metrics(query)

        query = "query=max(sum(rate(container_cpu_usage_seconds_total{pod_name=~\"%s.*\", container_name!=\"POD\"}[2m])) by (name)) * 100&" % self.query
        data["max"] = self.get_metrics(query)

        query = "query=min(sum(rate(container_cpu_usage_seconds_total{pod_name=~\"%s.*\", container_name!=\"POD\"}[2m])) by (name)) * 100&" % self.query
        data["min"] = self.get_metrics(query)
        return {"data": data}

    def units(self, interval=None):
        data = {"min": 0, "max": 100}
        query = "query=max(count(rate(container_memory_usage_bytes{pod_name=~\"%s.*\"}[2m])) by (slave))/2&" % self.query
        data["units"] = self.get_metrics(query)
        return {"data": data}

    def swap(self, interval=None):
        data = {"min": 0, "max": 1024}
        query = "query=avg(container_memory_swap{pod_name=~\"%s.*\", container_name!=\"POD\"})/1024/1024&" % self.query
        data["avg"] = self.get_metrics(query)

        query = "query=max(container_memory_swap{pod_name=~\"%s.*\", container_name!=\"POD\"})/1024/1024&" % self.query
        data["max"] = self.get_metrics(query)

        query = "query=min(container_memory_swap{pod_name=~\"%s.*\", container_name!=\"POD\"})/1024/1024&" % self.query
        data["min"] = self.get_metrics(query)
        return {"data": data}

    def netrx(self, interval=None):
        data = {"min": 0, "max": 100}
        query = "query=rate(container_network_receive_bytes_total{pod_name=~\"%s.*\"}[2m])/1024&" % self.query
        data["netrx"] = self.get_metrics(query)
        return {"data": data}

    def nettx(self, interval=None):
        data = {"min": 0, "max": 100}
        query = "query=rate(container_network_transmit_bytes_total{pod_name=~\"%s.*\"}[2m])/1024&" % self.query
        data["nettx"] = self.get_metrics(query)
        return {"data": data}

    def requests_min(self, interval=None):
        data = {}
        query = 'query=increase(nginx_upstream_requests_total{upstream=~\".*%s.*\", code="total"}[2m])/2&' % self.query
        data['requests'] = self.get_metrics(query)
        return {'data': data}

    def response_time(self, interval=None):
        data = {}
        query = 'query=nginx_upstream_response_msecs_avg{upstream=~\".*%s.*\"}/1000&' % self.query
        data['response'] = self.get_metrics(query)
        return {'data': data}

    def status_code(self, interval=None):
        data = {}
        query = 'query=increase(nginx_upstream_responses_total{upstream=~\".*%s.*\", status_code="1xx"}[2m])/2&' % self.query
        data["1xx"] = self.get_metrics(query)

        query = 'query=increase(nginx_upstream_responses_total{upstream=~\".*%s.*\", status_code="2xx"}[2m])/2&' % self.query
        data["2xx"] = self.get_metrics(query)

        query = 'query=increase(nginx_upstream_responses_total{upstream=~\".*%s.*\", status_code="3xx"}[2m])/2&' % self.query
        data["3xx"] = self.get_metrics(query)

        query = 'query=increase(nginx_upstream_responses_total{upstream=~\".*%s.*\", status_code="4xx"}[2m])/2&' % self.query
        data["4xx"] = self.get_metrics(query)

        query = 'query=increase(nginx_upstream_responses_total{upstream=~\".*%s.*\", status_code="5xx"}[2m])/2&' % self.query
        data["5xx"] = self.get_metrics(query)
        return {"data": data}

    def connections(self, interval=None):
        data = {"min": 0, "max": 100}
        query = 'query=count(container_network_tcp_usage_total{pod_name=~\"%s.*\",tcp_state="established"}) by (destination)&' % self.query
        data['connections'] = self.get_metrics(query)  # , processor=self.connections_processor)
        return {'data': data}

    def connections_processor(self, result):
        results = result.json()['data']['result']
        data = {}
        for r in results:
            data[base.set_destination_hostname(r['metric']['destination'])] = self.default_processor(r['values'])
        return data


class AppBackend(Prometheus):
    def __init__(self, app, url, process_name=None, date_range=None):
        query = '%s' % app["name"]
        if process_name is not None:
            query += '-%s' % process_name

        return super(AppBackend, self).__init__(
            url=url,
            query=query,
            date_range=date_range,
        )
