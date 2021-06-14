from django.db import models
from django.conf import settings
from django.utils.html import urlize
from django import forms
from django.utils import timezone
from rest_framework import serializers
from django.utils.html import escape


# Taking a time difference as inputs, it returns a string like:
# '223 days ago'
# '3 hours ago'
# '23 minutes ago'
# '20 seconds ago'
def x_ago_helper(diff):
    if diff.days > 0:
        return f'{diff.days} days ago'
    if diff.seconds < 60:
        return f'{diff.seconds} seconds ago'
    if diff.seconds < 3600:
        return f'{diff.seconds // 60} minutes ago'
    return f'{diff.seconds // 3600} hours ago'

def update_points_helper(obj):
    upvotes = obj.upvoted_users.filter(is_shadow_banned=False).distinct().count()
    downvotes = obj.downvoted_users.filter(is_shadow_banned=False).distinct().count()
    downvotes += obj.downvoted_users.filter(is_staff=True).count()
    obj.points = upvotes - downvotes
    obj.save()


def x_ago(obj):
    print("x_ago self.created:",obj.created)
    if obj.created=='':
        print("have no created date")
        return 0
    else:
        diff = timezone.now() - obj.created
        return x_ago_helper(diff)


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
    #body = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    created     = models.DateTimeField(editable=False,null=True)
    modified    = models.DateTimeField(null=True)
    answers_count = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    #hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    @property
    #not sure if need this
    def update_num_answers(self):
        comments = Comment.objects.filter(poster_id = self.id)
        self.answers_count = len(comments)
        self.save()

    def num_answers(self):
        comments = Comment.objects.filter(poster_id = self.id)
        return len(comments)

    def x_ago(self):
        print('poster x_ago--')
        return x_ago(self)
        # print("x_ago self.created:",self.created)
        # if self.created=='':
        #     print("have no created date")
        #     return 0
        # else:
        #     diff = timezone.now() - self.created
        #     return x_ago_helper(diff)

    def show_points(self):
        if self.points < 0:
            return 0
        else:
            return self.points

    def update_points(self):
        update_points_helper(self)
        
    def save(self, *args, **kwargs):
        print("poster save")
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Poster, self).save(*args, **kwargs)

    def show_points(self):
        if self.points < 0:
            return 0
        else:
            return self.points

    def __str__(self):
        return self.body


class Comment(models.Model):
    poster = models.ForeignKey(Poster, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #text = models.TextField()
    body = models.TextField(blank=True, null=True)
    created = models.DateTimeField(editable=False,null=True)
    modified = models.DateTimeField(null=True)
    points = models.IntegerField(default=0)
    #hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    @property
    def x_ago(self):
        print("comment x_ago")
        return x_ago(self)
        
    
    def update_points(self):
        update_points_helper(self)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

    def get_id(self):
        return self.id

    def __str__(self):
        return self.body


class UserField(serializers.Field):
    def to_representation(self, value):
        return value.username

    def to_internal_value(self, data):
        print("UserField to_internal_value")
        return data

class CommentSerializer(serializers.ModelSerializer):
    user = UserField()
    x_ago = serializers.SerializerMethodField()
    #poster = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = Comment
        fields = (
        'x_ago',
        'id',
        'body', 
        'points',
        'user', 
        )
    def get_x_ago(self, obj):
        return obj.x_ago





class PosterSerializer(serializers.ModelSerializer):
    user = UserField()
    comments = CommentSerializer(many=True, read_only=True)
    x_ago = serializers.SerializerMethodField()
    answers_count = serializers.SerializerMethodField()
    class Meta:
        model = Poster
        fields = (
        'x_ago',
        'id',
        'body', 
        'points',
        'created', 
        'user', 
        'answers_count',
        'comments'
        )
    def get_answers_count(self,obj):
        print('get_answers_count')
        return obj.num_answers()

    def get_x_ago(self, obj):
        print('poster get_x_ago object:',object)
        return obj.x_ago()

    def create(self, validated_data):
        print('create----',validated_data)
        #items_data = validated_data.pop('items')
        #print("items_data:",items_data)
        poster = Poster.objects.create(**validated_data)
            
        return poster





