# Generated by Django 3.2.3 on 2021-06-08 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20210528_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='poster',
            name='created',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='poster',
            name='modified',
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(editable=False, null=True)),
                ('modified', models.DateTimeField(null=True)),
                ('points', models.IntegerField(default=0)),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.poster')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]