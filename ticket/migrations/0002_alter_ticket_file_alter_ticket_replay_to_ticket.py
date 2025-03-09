# Generated by Django 4.2.20 on 2025-03-09 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media/ticket/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='replay_to_ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='ticket.ticket'),
        ),
    ]
