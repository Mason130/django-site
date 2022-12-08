# Generated by Django 4.1 on 2022-12-07 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pillrecognition', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pill_image', models.ImageField(blank=True, max_length=255, null=True, upload_to='uploaded_pill/image.png')),
            ],
        ),
    ]