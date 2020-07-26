import datetime
import random

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Min
from main.models import GeneratedQ

class Command(BaseCommand):

    help = "Tweet a question"

    def handle(self, *args, **options):
        oldest = datetime.date(year=1970, month=1, day=1)
        today = datetime.date.today()
        candidates = (GeneratedQ
                        .objects
                        .filter(tweeted=False, 
                                votes__gt=0,
                                displayed__gt=oldest,
                                displayed__lt=today)
                        .order_by("-votes"))
        if candidates:
            selected = candidates[0]
        # # tweet it
        # # tweeter.tweet(selected.text)

        