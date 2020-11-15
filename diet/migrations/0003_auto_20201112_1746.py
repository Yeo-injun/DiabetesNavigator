# Generated by Django 3.1.3 on 2020-11-12 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0002_auto_20201111_0008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food_nutrient',
            fields=[
                ('food_ID', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='음식ID')),
                ('food_name', models.CharField(max_length=50, verbose_name='음식명')),
                ('one_serving', models.IntegerField(verbose_name='1인분')),
                ('kcal', models.IntegerField(verbose_name='열량')),
                ('carbohydrate', models.IntegerField(verbose_name='탄수화물')),
                ('protein', models.IntegerField(verbose_name='단백질')),
                ('fat', models.IntegerField(verbose_name='지방')),
            ],
            options={
                'db_table': 'food_nutrients',
            },
        ),
        migrations.RenameModel(
            old_name='Meal_record_details',
            new_name='Food_detail',
        ),
        migrations.AlterModelTable(
            name='food_detail',
            table='food_details',
        ),
    ]