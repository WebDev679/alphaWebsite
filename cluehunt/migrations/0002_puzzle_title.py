# Generated by Django 2.2.14 on 2021-07-06 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cluehunt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='puzzle',
            name='title',
            field=models.CharField(blank=True, default='-', max_length=300, null=True),
        ),
    ]
