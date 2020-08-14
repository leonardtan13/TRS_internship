# Generated by Django 3.0.5 on 2020-06-26 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects_app', '0007_auto_20200624_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('PROPOSAL', 'Proposal'), ('IN_PROGRESS', 'In progress'), ('ENDED', 'Ended')], default='PROPOSAL', max_length=20),
        ),
    ]