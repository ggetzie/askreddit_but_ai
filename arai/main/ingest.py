from django.utils.text import slugify
from .models import TrainingQ, GeneratedQ

def save_training(filename):
    with open(filename) as question_file:
        lines = question_file.readlines()
        questions = [TrainingQ(text=line, slug=slugify(line)) 
                    for line in lines]
        TrainingQ.objects.bulk_create(questions, ignore_conflicts=True)

def save_generated(filename):
    with open(filename) as question_file:
        lines = question_file.readlines()
        training = set([t.slug for t in TrainingQ.objects.all()])
        questions = [GeneratedQ(text=line, slug=slugify(line))
                     for line in lines if not slugify(line) in training]
        GeneratedQ.objects.bulk_create(questions, ignore_conflicts=True)

