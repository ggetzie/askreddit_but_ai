import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView, DetailView


from .models import GeneratedQ, About

@method_decorator(ensure_csrf_cookie, name="dispatch")
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

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(*args, **kwargs)
        context["vote_states"] = json.dumps((self
                                             .request
                                             .session.get("vote_states", {})))
        try:                                        
            context["latest_tweet"] = (GeneratedQ
                                        .objects
                                        .filter(tweeted=True)
                                        .latest("tweet_time"))
        except GeneratedQ.DoesNotExist:
            pass
        
        return context

class AboutView(DetailView):
    model = About
    template_name = "main/about.html"

    def get_object(self, queryset=None):
        about = get_object_or_404(About, published=True)
        return about

class Archive(ListView):
    model = GeneratedQ
    paginate_by = 50
    template_name = "main/archive.html"

    def get_queryset(self):
        oldest = datetime.date(year=1970, month=1, day=1)
        qs = (GeneratedQ.objects.exclude(displayed=oldest)
                                .order_by("-displayed").distinct("displayed"))
        return qs

    
@require_POST
def cast_vote(request):
    
    data = json.loads(request.body)
    q_id = data.get("question_id", -1)
    direction = data.get("direction", "")

    try:
        question = GeneratedQ.objects.get(id=q_id)
    except GeneratedQ.DoesNotExist:
        return JsonResponse({"error": "Couldn't find that question"})
    v_id = f"vote{q_id}"
    vote_states = request.session.get("vote_states", {})
    # Store the current user's vote in session
    # A value of 1 means they have voted up and cannot vote further up
    # but they can still vote down
    # A value of -1 means they have voted down and cannot vote further down
    # but they can still vote up
    # 0 or no value means they can vote up or down
    previous = vote_states.get(v_id, 0)
    if direction == "up":
        if previous == 1:
            # remove existing upvote
            vote_states[v_id] = 0
            question.votes -= 1
        elif previous == -1:
            # replace existing upvote with a downvote
            vote_states[v_id] = 1
            question.votes += 2
        else:
            # new upvote
            vote_states[v_id] = 1
            question.votes += 1
    elif direction == "down":
        if previous == -1:
            # remove existing downvote
            vote_states[v_id] = 0
            question.votes += 1
        elif previous == 1:
            # replace existing upvote with a downvote
            vote_states[v_id] = -1
            question.votes -= 2
        else:
            # new downvote
            vote_states[v_id] = -1
            question.votes -= 1
    else:
        vote_states[v_id] = 0
    question.save()
    request.session["vote_states"] = vote_states

    return JsonResponse({
                        "result": "success",
                        "question_id": q_id,
                        "vote_state": vote_states[v_id]
                        })
    


