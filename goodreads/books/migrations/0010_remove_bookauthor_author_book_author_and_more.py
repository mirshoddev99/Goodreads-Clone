# Generated by Django 4.1.2 on 2022-11-16 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_rename_starts_given_bookreview_stars_given'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookauthor',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='books.author'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='author',
            name='bio',
            field=models.TextField(default='', editable=False),
        ),
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(default='', editable=False, max_length=254),
        ),
        migrations.AlterField(
            model_name='author',
            name='first_name',
            field=models.CharField(default='', editable=False, max_length=100),
        ),
        migrations.AlterField(
            model_name='author',
            name='last_name',
            field=models.CharField(default='', editable=False, max_length=100),
        ),
    ]
