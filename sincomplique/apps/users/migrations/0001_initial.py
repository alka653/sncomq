# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileUser',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('cc', models.CharField(max_length=15)),
                ('telefono', models.CharField(max_length=10)),
                ('cc_residencia', models.ForeignKey(related_name='cc_residencia', to='principal.Municipio')),
                ('ciudad', models.ForeignKey(related_name='ciudad_residencia', to='principal.Municipio')),
            ],
        ),
    ]
