# Generated by Django 4.2.2 on 2023-08-07 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_remove_user_isprovider'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='time_completed',
        ),
    ]
