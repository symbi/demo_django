from django.db import models
from django.contrib.auth.models import AbstractUser
#from main.models import Question, Answer
from main.models import Team, Poster, Comment
from functools import reduce
from django.db.models import Q
#from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer


class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
    points = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    upvoted_posts = models.ManyToManyField(Poster, related_name="upvoted_users")
    upvoted_comments = models.ManyToManyField(Comment, related_name="upvoted_users")
    

# class CustomUserCreateSerializer(UserCreateSerializer):
#     class Meta:
#         fields = tuple(User.REQUIRED_FIELDS) + (
#             User.USERNAME_FIELD, User._meta.pk.name, 'password',
#             'is_manager',
#         )

# class CustomUserSerializer(UserSerializer):
#     class Meta:
#         model = User
#         fields = tuple(User.REQUIRED_FIELDS) + (
#             User._meta.pk.name,
#             User.USERNAME_FIELD,
#             'is_manager',
#         )
#         read_only_fields = (User.USERNAME_FIELD,)