# Generated by Django 3.2.18 on 2023-03-31 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../https://res.cloudinary.com/dqgs0kltd/image/upload/v1673026752/sample.jpg', upload_to='images/'),
        ),
    ]
