import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import GeneratedQ

class QuestionList(ListView):
    model = GeneratedQ
    paginate_by = 50
    template_name = "main/question_list.html"

    def get_queryset(self):
        if "date" in self.kwargs:
            date = datetime.datetime.strptime(self.kwargs["date"],
                                              "%Y%m%d")
        else:
            date = datetime.date.today()
                        
        qs = self.model.objects.filter(displayed=date)
        return qs

def cast_vote(request):
    return JsonResponse({"result": "ok"})
    


