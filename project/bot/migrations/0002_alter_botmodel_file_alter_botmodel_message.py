# Generated by Django 4.2.6 on 2023-10-13 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botmodel',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='botmodel',
            name='message',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
