import datetime
import json
import logging

import requests
from requests_oauthlib import OAuth1Session

from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.management.base import BaseCommand
from main.models import GeneratedQ

ARAI_REDDIT_ID = settings.ARAI_REDDIT_ID
ARAI_REDDIT_SECRET = settings.ARAI_REDDIT_SECRET
ARAI_REDDIT_PASSWORD = settings.ARAI_REDDIT_PASSWORD
ARAI_REDDIT_USERNAME = settings.ARAI_REDDIT_USERNAME
ARAI_REDDIT_UA = settings.ARAI_REDDIT_UA

TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
POST_URL = "https://oauth.reddit.com/api/submit"
logger = logging.getLogger(__name__)


def get_reddit_token():
    client_auth = requests.auth.HTTPBasicAuth(ARAI_REDDIT_ID, ARAI_REDDIT_SECRET)
    post_data = {
        "grant_type": "password",
        "username": ARAI_REDDIT_USERNAME,
        "password": ARAI_REDDIT_PASSWORD,
    }
    headers = {"User-Agent": ARAI_REDDIT_UA}
    response = requests.post(
        TOKEN_URL, auth=client_auth, data=post_data, headers=headers, timeout=10
    )
    rj = response.json()
    return rj["access_token"]


def post_to_reddit(title, token):
    headers = {"Authorization": f"bearer {token}", "User-Agent": ARAI_REDDIT_UA}
    post_title = title if title.endswith("?") else title + "?"
    post_data = {
        "ad": False,
        "api_type": "json",
        "app": ARAI_REDDIT_ID,
        "extension": "json",
        "kind": "self",
        "nsfw": False,
        "resubmit": False,
        "sendreplies": False,
        "spoiler": False,
        "sr": "AskRedditButAI",
        "text": "",
        "title": post_title,
    }
    response = requests.post(POST_URL, headers=headers, data=post_data, timeout=10)
    return response


def create_tweet(
    consumer_key, consumer_secret, access_token, access_token_secret, message
):
    payload = {"text": message}
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )
    response = oauth.post("https://api.twitter.com/2/tweets", json=payload)

    return response


class Command(BaseCommand):
    help = "Tweet highest voted question that hasn't been tweeted"

    def handle(self, *args, **options):
        oldest = datetime.date(year=1970, month=1, day=1)
        today = datetime.date.today()
        candidates = GeneratedQ.objects.filter(
            tweeted=False, votes__gt=0, displayed__gt=oldest, displayed__lt=today
        ).order_by("-votes")
        if candidates:
            selected = candidates[0]
            response = create_tweet(
                settings.ARAI_TWITTER_API_KEY,
                settings.ARAI_TWITTER_API_SECRET_KEY,
                settings.ARAI_TWITTER_ACCESS_TOKEN,
                settings.ARAI_TWITTER_ACCESS_TOKEN_SECRET,
                selected.text,
            )
            if response.status_code != 201:
                logger.error(
                    "Error sending tweet: %s %s", response.status_code, response.content
                )

            else:
                logger.info(
                    "Tweet sent: %s %s",
                    response.status_code,
                    json.dumps(response.json(), indent=2, sort_keys=True),
                )
                selected.tweeted = True
                selected.tweet_time = datetime.datetime.now(tz=datetime.timezone.utc)

            cache_key = make_template_fragment_key("latest_tweet")
            cache.delete(cache_key)

            # Post to AskReddit
            # Sample response:
            # {'json': {'errors': [],
            #           'data': {'url': 'https://www.reddit.com/r/AskRedditButAI/comments/ia5zct/test_post_please_ignore/.json',
            #                    'drafts_count': 0,
            #                    'id': 'ia5zct',
            #                    'name': 't3_ia5zct'}}}

            token = get_reddit_token()
            response = post_to_reddit(selected.text, token)
            if response.status_code == 200:
                selected.submitted = True
                selected.submit_time = datetime.datetime.now(tz=datetime.timezone.utc)
                rj = response.json()
                selected.reddit_id = rj["json"]["data"]["id"]

            selected.save()
