# Generated by Django 3.1.1 on 2020-09-28 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20200928_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='jobs.category'),
        ),
    ]
