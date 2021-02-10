# Generated by Django 3.0.8 on 2021-02-10 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0005_auto_20210210_1640'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Laptop',
            new_name='Device',
        ),
        migrations.DeleteModel(
            name='Desktop',
        ),
        migrations.DeleteModel(
            name='Mobile',
        ),
        migrations.AlterModelOptions(
            name='device',
            options={'ordering': ['-id']},
        ),
        migrations.AlterUniqueTogether(
            name='device',
            unique_together={('VT_Tag', 'CS_Tag')},
        ),
    ]
