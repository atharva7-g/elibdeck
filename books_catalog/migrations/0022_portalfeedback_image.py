# Generated by Django 5.1.4 on 2025-01-08 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_catalog', '0021_alter_book_publication_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='portalfeedback',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='feedback_images/'),
        ),
    ]
