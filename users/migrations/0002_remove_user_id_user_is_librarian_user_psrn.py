# Generated by Django 5.1.4 on 2024-12-26 09:48

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AddField(
            model_name='user',
            name='is_librarian',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='psrn',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False, null=True),
        ),
    ]
