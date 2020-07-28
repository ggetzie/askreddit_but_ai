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
    if not request.POST:
        return JsonResponse({"error": "invalid request"})
    data = request.POST.copy()
    q_id = data.get("question_id", -1)
    direction = data.get("direction", "")

    try:
        question = GeneratedQ.objects.get(id=q_id)
    except GeneratedQ.DoesNotExist:
        return JsonResponse({"error": "Couldn't find that question"})
    v_id = f"vote{q_id}"
    # Store the current user's vote in session
    # A value of 1 means they have voted up and cannot vote further up
    # but they can still vote down
    # A value of -1 means they have voted down and cannot vote further down
    # but they can still vote up
    # 0 or no value means they can vote up or down
    previous = request.session.get(v_id, 0)
    if direction == "up":
        if previous == 1:
            request.session[v_id] = 0
            GeneratedQ.votes -= 1
        else:
            request.session[v_id] = 1
            GeneratedQ.votes += 1
    elif direction == "down":
        if previous == -1:
            request.session[v_id] = 0
            GeneratedQ.votes += 1
        else:
            request.session[v_id] = -1
            GeneratedQ.votes -= 1
    else:
        request.session[v_id] = 0
    GeneratedQ.save()

    return JsonResponse({
                            "result": "success",
                            "question_id": q_id,
                            "vote_state": request.session[v_id]
                        })
    


