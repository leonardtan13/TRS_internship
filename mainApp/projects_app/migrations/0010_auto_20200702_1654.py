# Generated by Django 3.0.7 on 2020-07-02 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects_app', '0009_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default='', max_length=240)),
                ('value', models.CharField(default='', max_length=240)),
            ],
        ),
        migrations.CreateModel(
            name='TableDictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('domain_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects_app.Domain')),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects_app.Project')),
            ],
            options={
                'verbose_name': 'Table',
                'verbose_name_plural': 'Tables',
            },
        ),
        migrations.DeleteModel(
            name='Table',
        ),
        migrations.AddField(
            model_name='keyvalue',
            name='table_dictionary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects_app.TableDictionary'),
        ),
    ]
