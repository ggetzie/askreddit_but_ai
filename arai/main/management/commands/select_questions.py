import datetime
import random

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Min
from main.models import GeneratedQ

DAILY_COUNT = 25


class Command(BaseCommand):
    help = f"Selects {DAILY_COUNT} random questions to display each day"

    def handle(self, *args, **options):
        min_date = GeneratedQ.objects.filter(tweeted=False, votes=0).aggregate(
            Min("displayed")
        )["displayed__min"]
        today = datetime.date.today()
        print(f"### Selecting questions for {today}")
        # Find oldest questions that haven't been tweeted or voted on
        candidates = GeneratedQ.objects.filter(
            displayed=min_date, tweeted=False, votes=0
        ).order_by("randomized")
        print(f"Found {candidates.count()} candidates")
        # We should have lots if we haven't gotten through all the questions
        # yet. (min_date = Jan 1, 1970)
        # If we are recycling, there should only be DAILY_COUNT questions
        # at min_date
        num_questions = min(DAILY_COUNT, candidates.count())
        for q in candidates[:num_questions]:
            q.displayed = today
            print(q.text)
            q.save()
        print()
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        old_pages = (
            GeneratedQ.objects.filter(displayed=yesterday).count() // DAILY_COUNT
        )
        for i in range(1, old_pages + 1):
            cache_key = make_template_fragment_key(
                "question_list", [yesterday.isoformat(), i]
            )
            cache.delete(cache_key)
