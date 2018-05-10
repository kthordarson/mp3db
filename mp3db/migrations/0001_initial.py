# Generated by Django 2.0.4 on 2018-05-08 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_id', models.IntegerField()),
                ('album_title', models.CharField(max_length=255)),
                ('artist_id', models.IntegerField()),
                ('albumartist_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='albumartist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('albumartist_id', models.IntegerField()),
                ('albumartist_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_id', models.IntegerField()),
                ('artist_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_id', models.IntegerField()),
                ('filename', models.CharField(max_length=255)),
                ('filehash', models.CharField(max_length=255)),
                ('size', models.IntegerField()),
                ('album_title', models.CharField(max_length=255)),
                ('artist_name', models.CharField(max_length=255)),
                ('albumartist_name', models.CharField(max_length=255)),
                ('song_title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_id', models.IntegerField()),
                ('file_id', models.IntegerField()),
                ('artist_id', models.IntegerField()),
                ('albumartist_id', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
            ],
        ),
    ]
