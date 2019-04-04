from django.db import models
from datetime import datetime

# Create your models here.
# Every model will inherit for django's base model

# Everytime you add or change a model, you have to make migrations and then migrate

class TutorialCategory(models.Model):
  tutorial_category = models.CharField(max_length=200)
  category_summary = models.CharField(max_length=200)
  category_slug = models.CharField(max_length=200) # for url

  class Meta:
    verbose_name_plural = "Categories" # to override the admin naming 

  def __str__(self):
    return self.tutorial_category

class TutorialSeries(models.Model):
  tutorial_series = models.CharField(max_length=200)

  # create key to tutorial catergory
  tutorial_category = models.ForeignKey(TutorialCategory, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
  series_summary = models.CharField(max_length=200)

  class Meta:
    verbose_name_plural = "Series"

  def __str__(self):
    return self.tutorial_series

# foreign key for pointing tutorial to a series then to the tutorial category

class Tutorial(models.Model):
  # specifying columns we want in our tutorial
  tutorial_title = models.CharField(max_length=200)
  tutorial_content = models.TextField() # used for something of not finite length
  tutorial_published = models.DateTimeField("date published", default=datetime.now())

  # create key to tutorial series
  tutorial_series = models.ForeignKey(TutorialSeries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)

  # url for the tutorial itself
  tutorial_slug = models.CharField(max_length=200, default=1)

  # can do various overrides like the string method
  def __str__(self):
    return self.tutorial_title


  # models map to a database table