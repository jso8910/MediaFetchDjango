# Generated by Django 3.2.2 on 2021-05-14 07:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210514_0656'),
    ]

    operations = [
        migrations.AddField(
            model_name='queries',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]