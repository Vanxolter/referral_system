# Generated by Django 5.1.3 on 2024-12-02 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_users_phone_n_a3b1c5_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='invite_code',
            field=models.CharField(default='IxhgXF', editable=False, max_length=6, unique=True),
        ),
    ]