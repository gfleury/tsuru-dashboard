from tsuru_dashboard import engine
import tsuru_dashboard.autoscale

class ResourcesTab(engine.Tab):
    name = 'resources'
    url_name = 'detail-app'


class DeploysTab(engine.Tab):
    name = 'deploys'
    url_name = 'app-deploys'


class EventsTab(engine.Tab):
    name = 'events'
    url_name = 'app-events'


class LogTab(engine.Tab):
    name = 'log'
    url_name = 'app_log'


class SettingsTab(engine.Tab):
    name = 'settings'
    url_name = 'app-settings'


class AutoScaleTab(engine.Tab):
    name = 'autoscale'
    url_name = 'autoscale-app-info'


class App(engine.App):
    name = 'app'

    def __init__(self):
        self.tabs = [ResourcesTab, DeploysTab, EventsTab, LogTab, SettingsTab, AutoScaleTab]


engine.register(App)
