import datetime
import logging

import requests
import tweepy

from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Min
from main.models import GeneratedQ

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    help = "Tweet highest voted question that hasn't been tweeted"

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
        print(f"candidates: {candidates}")
        if candidates:
            selected = candidates[0]
            auth = tweepy.OAuthHandler(settings.ARAI_TWITTER_API_KEY, 
                                       settings.ARAI_TWITTER_API_SECRET_KEY)
            auth.set_access_token(settings.ARAI_TWITTER_ACCESS_TOKEN, 
                                  settings.ARAI_TWITTER_ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth, 
                             wait_on_rate_limit=True,
                             wait_on_rate_limit_notify=True)
            try:
                response = api.update_status(selected.text)
                print(response)
            except Exception as e:
                print(e)
                logger.error("Error posting tweet", exc_info=True)
            selected.tweeted = True
            selected.tweet_time = datetime.datetime.now(tz=datetime.timezone.utc)
            selected.save()
            cache_key = make_template_fragment_key("latest_tweet")
            cache.delete(cache_key)

        