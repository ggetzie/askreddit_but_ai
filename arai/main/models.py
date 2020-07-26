import datetime

from django.db import models
from django.utils.text import slugify

class TrainingQ(models.Model):
    text = models.CharField("Text", 
                            max_length=340,
                            default="",
                            blank=True)
    slug = models.SlugField("Slug",
                            max_length=340,
                            default="",
                            unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.text)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:20]


class GeneratedQ(models.Model):
    text = models.CharField("Text",
                            max_length=280,
                            default="",
                            blank=True)
    slug = models.SlugField("Slug",
                            max_length=280,
                            default="",
                            unique=True)
    displayed = models.DateField("Last Displayed",
                                 default=datetime.date(year=1970,
                                                       month=1,
                                                       day=1)) 
    tweeted = models.BooleanField("Tweeted", 
                                  default=False)
    votes = models.IntegerField("Votes", default=0)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.text)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:20]