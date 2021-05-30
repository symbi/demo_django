from django.db import models
from django.conf import settings
from django.utils.html import urlize
from django import forms
from django.utils import timezone
from rest_framework import serializers
from django.utils.html import escape

class Team(models.Model):
    name=models.CharField(max_length=100)
    slug=models.CharField(max_length=100)

    def get_absolute_url(self):
        return f'/{self.slug}/'

    def __str__(self):
        return self.name

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "slug",
        )


def x_ago_helper(diff):
    if diff.days > 0:
        return f'{diff.days} days ago'
    if diff.seconds < 60:
        return f'{diff.seconds} seconds ago'
    if diff.seconds < 3600:
        return f'{diff.seconds // 60} minutes ago'
    return f'{diff.seconds // 3600} hours ago'

class Test(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'

class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "get_absolute_url",
        )


           
class Poster(models.Model):
    #other=models.ForeignKey(Other, on_delete=models.CASCADE, default=Other.DEFAULT_PK)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=0)
    #slug = models.SlugField()
    #title = models.CharField(max_length=200, null=True)
    body = models.TextField(blank=True, null=True)
    #created     = models.DateTimeField(editable=False)
    #modified    = models.DateTimeField()
    answers_count = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    #hidden = models.BooleanField(default=False)


    @property
    # def x_ago(self):
    #     diff = timezone.now() - self.created
    #     return x_ago_helper(diff)
    def show_points(self):
        if self.points < 0:
            return 0
        else:
            return self.points

    def __str__(self):
        return self.body

class UserField(serializers.Field):
    def to_representation(self, value):
        return value.username

class PosterSerializer(serializers.ModelSerializer):
    #user = UserField()
    #x_ago = serializers.SerializerMethodField()
    #answers_count = serializers.SerializerMethodField()
    class Meta:
        model = Poster
        fields = (
        #'x_ago',
        'id',
        'body', 
        #'points',
        #'created', 
        #'user', 
        #'answers_count',
        )#
    # def get_answers_count(self,obj):
    #     print('get_answers_count')
    #     return obj.num_answers()
    # def get_x_ago(self, obj):
    #     print('get x ago')
    #     return x_ago_helper(timezone.now() - obj.created)

    def create(self, validated_data):
        print('create----',validated_data)
        #items_data = validated_data.pop('items')
        #print("items_data:",items_data)
        poster = Poster.objects.create(**validated_data)
            
        return poster




