# Generated by Django 4.2 on 2023-05-28 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_category_active_alter_category_favourite_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='catalog.product'),
        ),
    ]
