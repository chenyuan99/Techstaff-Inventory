# Generated by Django 3.0.8 on 2021-03-02 22:54

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('Manufacturer', models.CharField(default='', max_length=100)),
                ('Model', models.CharField(default='', max_length=100)),
                ('VT_Tag', models.CharField(default='', max_length=100)),
                ('CS_Tag', models.CharField(default='', max_length=100)),
                ('Serial_Number', models.CharField(default='', max_length=100)),
                ('status', models.CharField(choices=[('AVAILABLE', 'Item ready to be purchased'), ('SOLD', 'Item Sold'), ('RESTOCKING', 'Item restocking in few days')], default='SOLD', max_length=10)),
                ('issue', models.CharField(default='No issues', max_length=100)),
            ],
            options={
                'ordering': ['-id'],
                'unique_together': {('VT_Tag', 'CS_Tag')},
            },
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realname', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=16)),
                ('email', models.EmailField(max_length=254)),
                ('sign', models.BooleanField()),
                ('create_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Hostname',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Hostname', models.CharField(max_length=64)),
                ('Aliases', models.CharField(max_length=64)),
                ('IP_Address', models.CharField(max_length=64)),
                ('IPv6_Address', models.CharField(max_length=64)),
                ('MAC_Address', models.CharField(max_length=64)),
                ('create_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('guest_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hello.Guest')),
            ],
            bases=('hello.guest',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('guest_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hello.Guest')),
            ],
            bases=('hello.guest',),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('notes', models.CharField(max_length=200)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(choices=[('AVAILABLE', 'Item ready to be purchased'), ('SOLD', 'Item Sold'), ('RESTOCKING', 'Item restocking in few days')], default='SOLD', max_length=10)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.Device')),
                ('hostname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.Hostname')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.Faculty')),
            ],
        ),
        migrations.AddField(
            model_name='faculty',
            name='assigned_student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.Student'),
        ),
    ]
