# Generated by Django 4.2 on 2023-05-24 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_uploadcsv_cases_alter_uploadcsv_death_cases_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CaseData',
        ),
        migrations.DeleteModel(
            name='CasesData',
        ),
        migrations.DeleteModel(
            name='DeathData',
        ),
        migrations.DeleteModel(
            name='DeathsData',
        ),
        migrations.DeleteModel(
            name='MalariaData',
        ),
        migrations.DeleteModel(
            name='SevereData',
        ),
    ]