# Generated by Django 4.2.13 on 2024-06-04 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0002_alter_message_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'permissions': [('can_edit_message', 'Can edit message'), ('can_delete_message', 'Can delete message')]},
        ),
    ]
