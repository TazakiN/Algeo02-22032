# Generated by Django 4.2.7 on 2023-11-17 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0004_rename_image_imagequery'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='h0',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='h1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='h2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='h3',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='h4',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='h5',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='h6',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='h7',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='s0',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='s1',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='s2',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='v0',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='v1',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='dataset',
            name='v2',
            field=models.FloatField(default=0.0),
        ),
    ]