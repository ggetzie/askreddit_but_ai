import datetime
import random

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Min
from main.models import GeneratedQ

class Command(BaseCommand):

    help = "Selects 50 random questions to display each day"

    def handle(self, *args, **options):
        min_date = (GeneratedQ
                    .objects
                    .filter(tweeted=False, votes=0)
                    .aggregate(Min("displayed"))["displayed__min"])

        candidates = GeneratedQ.objects.filter(displayed=min_date, 
                                               tweeted=False,
                                               votes=0)
        if candidates.count() == 50:
            candidates.update(displayed=datetime.date.today())
        else:
            today = datetime.date.today()
            selected = random.sample(list(candidates), 50)
            for q in selected:
                q.displayed=today
            GeneratedQ.objects.bulk_update(selected, ["displayed"])
        yesterday = datetime.date.today - datetime.timedelta(days=1)
        cache_key = make_template_fragment_key("question_list", [yesterday.isoformat()])
        cache.delete(cache_key)