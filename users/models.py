from django.db import models
from django.contrib.auth.models import AbstractUser
#from main.models import Question, Answer
from main.models import Team
from functools import reduce
from django.db.models import Q

class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
    points = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
