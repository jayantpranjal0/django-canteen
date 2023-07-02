# Generated by Django 4.2.2 on 2023-07-02 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='canteen',
            name='meals',
        ),
        migrations.AddField(
            model_name='meal',
            name='canteen',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='base.canteen'),
            preserve_default=False,
        ),
    ]