# Generated by Django 3.2.7 on 2021-09-26 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0002_auto_20210926_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='jakmallscrapper',
            name='pid',
            field=models.IntegerField(default=0),
        ),
    ]