# Generated by Django 2.1.7 on 2019-03-12 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_name', models.CharField(max_length=250)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('data_type', models.CharField(max_length=100)),
            ],
        ),
    ]
