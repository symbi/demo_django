# Generated by Django 3.2.4 on 2021-06-15 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210614_1234'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='upvoted_comments',
            field=models.ManyToManyField(related_name='upvoted_users', to='main.Comment'),
        ),
        migrations.AddField(
            model_name='user',
            name='upvoted_posts',
            field=models.ManyToManyField(related_name='upvoted_users', to='main.Poster'),
        ),
    ]
