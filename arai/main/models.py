import datetime

import markdown

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from django.utils.text import slugify

DEFAULT_DT = datetime.datetime(year=1970, month=1, day=1, tzinfo=datetime.timezone.utc)


class TrainingQ(models.Model):
    text = models.CharField("Text", max_length=340, default="", blank=True)
    slug = models.SlugField("Slug", max_length=340, default="", unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.text)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:20]


class GeneratedQ(models.Model):
    text = models.CharField("Text", max_length=280, default="", blank=True)
    slug = models.SlugField("Slug", max_length=280, default="", unique=True)
    displayed = models.DateField(
        "Last Displayed", default=datetime.date(year=1970, month=1, day=1)
    )
    tweeted = models.BooleanField("Tweeted", default=False)
    tweet_time = models.DateTimeField("Time when Tweeted", default=DEFAULT_DT)
    votes = models.IntegerField("Votes", default=0)
    randomized = models.PositiveIntegerField("Random Order", default=1)
    submitted = models.BooleanField("Submitted to Reddit", default=False)
    submit_time = models.DateTimeField("Time when Submitted", default=DEFAULT_DT)
    reddit_id = models.CharField("Reddit Post Id", default="", max_length=30)

    class Meta:
        ordering = ["slug"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.text)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:20]


class About(models.Model):
    text = models.TextField("About Text")
    html = models.TextField("About Html")
    published = models.BooleanField("Published", default=False)
    title = models.CharField("Title", default="", max_length=30, unique=True)

    def __str__(self):
        return self.text[:20]

    def save(self, *args, **kwargs):
        self.html = markdown.markdown(self.text)
        cache_key = make_template_fragment_key("about", [self.title])
        cache.delete(cache_key)
        return super().save(*args, **kwargs)
