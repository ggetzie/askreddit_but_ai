from django.urls import include, path, register_converter
from django.views.generic import TemplateView

import main.views as views

app_name = "main"

class DateConverter:
    regex = '[0-9]{8}'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return '%08d' % value

register_converter(DateConverter, "yyyymmdd")

urlpatterns = [
    path("", views.QuestionList.as_view(), name="home"),
    path("<yyyymmdd:date>", views.QuestionList.as_view(), name="on_date")
]