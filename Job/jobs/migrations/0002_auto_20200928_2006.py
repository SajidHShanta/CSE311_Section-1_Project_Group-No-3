# Generated by Django 3.1.1 on 2020-09-28 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(default=None, editable=False)),
            ],
        ),
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ('-id',)},
        ),
        migrations.AddField(
            model_name='job',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='jobs.category'),
        ),
    ]
