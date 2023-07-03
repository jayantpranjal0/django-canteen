# Generated by Django 4.2.2 on 2023-07-03 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_rename_completedorders_completedorder_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='completedorderitem',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='completedorderitem',
            name='meal',
        ),
        migrations.RemoveField(
            model_name='completedorderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='canteen',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='user',
            name='default_organization',
        ),
        migrations.RemoveField(
            model_name='user',
            name='organizations',
        ),
        migrations.AddField(
            model_name='order',
            name='canteen',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.canteen'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='base.OrderItem', to='base.meal'),
        ),
        migrations.AddField(
            model_name='order',
            name='time_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='time_completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity_delivered',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity_ordered',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='default_canteen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.canteen'),
        ),
        migrations.AlterField(
            model_name='user',
            name='favourite_canteen',
            field=models.ManyToManyField(blank=True, related_name='+', to='base.canteen'),
        ),
        migrations.DeleteModel(
            name='CompletedOrder',
        ),
        migrations.DeleteModel(
            name='CompletedOrderItem',
        ),
        migrations.DeleteModel(
            name='Organization',
        ),
    ]
