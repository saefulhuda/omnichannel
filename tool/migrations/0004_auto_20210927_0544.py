# Generated by Django 3.2.7 on 2021-09-26 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0003_jakmallscrapper_pid'),
    ]

    operations = [
        migrations.AddField(
            model_name='jakmallscrapper',
            name='long_desc',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='jakmallscrapper',
            name='short_desc',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
