# Generated by Django 4.0 on 2024-10-13 00:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('created_at', models.DateField(auto_created=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('Updated_at', models.DateField(auto_now_add=True)),
                ('description', models.CharField(max_length=100)),
                ('amount', models.FloatField(max_length=100)),
            ],
            options={
                'ordering': ('description',),
            },
        ),
    ]
