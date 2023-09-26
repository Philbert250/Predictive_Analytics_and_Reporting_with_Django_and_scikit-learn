from django.db import models
from django_pandas.managers import DataFrameManager

# Create your models here.
class GeneralData(models.Model):
    year = models.CharField(max_length=250)
    casename = models.CharField(max_length=250)
    value = models.FloatField()

    objects = DataFrameManager()

class Uploadcsv(models.Model):
    year = models.CharField(max_length=255, default="")
    province_name = models.CharField(max_length=250, default="")
    cases = models.CharField(max_length=255, default="")
    death_cases = models.CharField(max_length=255, default="")

    objects = DataFrameManager()
    def __str__(self):
        return self.year
