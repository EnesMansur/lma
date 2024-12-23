# Generated by Django 4.2.17 on 2024-12-23 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
        ('membership', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated At')),
                ('borrow_date', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('return_date', models.DateField(blank=True, null=True)),
                ('book_edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.bookedition')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
