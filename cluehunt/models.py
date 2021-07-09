from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Puzzle(models.Model):
    code = models.CharField(null=True, blank=True, max_length=300)
    resources = models.TextField(blank=True, null=True, default='--')
    level = models.IntegerField(blank=True, null=True, default=0)
    hints = models.TextField(blank=True, null=True, default='--')
    hintNumber = models.IntegerField(blank=True, null=True, default=1)
    title = models.CharField(blank=True, null=True, default='-', max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.level)

class School(models.Model):
    name = models.CharField(null=True, blank=True, max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.IntegerField(blank=True, null=True, default=0)
    submission_time = models.DateTimeField(null=True, blank=True)
    skipsLeft = models.IntegerField(null=True, blank=True, default=1)
    hintsLeft = models.IntegerField(null=True, blank=True, default=3)

    def __str__(self):
        return self.name