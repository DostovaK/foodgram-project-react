# Generated by Django 2.2.16 on 2022-11-29 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20221127_2115'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorite',
            name='unique_favourite',
        ),
    ]
