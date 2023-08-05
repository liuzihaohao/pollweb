# Generated by Django 3.2 on 2023-08-05 02:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('public_grade', models.CharField(choices=[('A', 'public_disclosure'), ('B', 'partial_disclosure'), ('C', 'internal_disclosure'), ('D', 'partial_internal_disclosure'), ('E', 'internal_confidentiality'), ('F', 'strictly_confidential'), ('G', 'system_confidentiality')], max_length=1)),
                ('is_all_registered', models.BooleanField()),
                ('question_list', models.TextField()),
                ('create_data', models.DateTimeField()),
                ('last_change_data', models.DateTimeField()),
                ('is_active', models.BooleanField()),
                ('admins', models.ManyToManyField(related_name='alladmins', to=settings.AUTH_USER_MODEL)),
                ('registered_list', models.ManyToManyField(related_name='allregistered', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('answer_list', models.TextField()),
                ('public_grade_u', models.CharField(choices=[('A', 'public'), ('B', 'public_to_staff'), ('C', 'secrecy')], max_length=1)),
                ('create_data', models.DateTimeField()),
                ('last_change_data', models.DateTimeField()),
                ('from_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.activity')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
