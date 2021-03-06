# Generated by Django 2.1.4 on 2019-01-01 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateField()),
                ('score', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenge.ScoringItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenge.User')),
            ],
        ),
    ]
