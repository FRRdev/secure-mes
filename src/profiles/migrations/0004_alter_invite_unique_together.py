# Generated by Django 4.0.4 on 2022-04-22 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_invite_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='invite',
            unique_together=set(),
        ),
    ]
