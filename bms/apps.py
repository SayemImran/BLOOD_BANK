from django.apps import AppConfig


class BmsConfig(AppConfig):
    name = 'bms'
    def ready(self):
        import bms.signals