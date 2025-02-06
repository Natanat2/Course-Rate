from django.db import models


class CourseRateUsd(models.Model):
    course = models.FloatField(max_length = 8, blank = False, null = False)
    updated_at = models.DateTimeField()
