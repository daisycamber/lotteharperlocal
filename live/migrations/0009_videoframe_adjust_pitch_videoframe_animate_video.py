# Generated by Django 5.1.7 on 2025-03-21 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live', '0008_rename_default_videocamera_adjust_pitch_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoframe',
            name='adjust_pitch',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='videoframe',
            name='animate_video',
            field=models.BooleanField(default=False),
        ),
    ]
