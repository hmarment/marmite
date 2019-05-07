import os

from django.apps import AppConfig


class GuardianConfig(AppConfig):
    name = "guardian"
    API_KEY = os.environ["GUARDIAN_API_KEY"]
