# Generated by Django 2.2 on 2019-04-10 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("recipes", "0002_auto_20190410_2025")]

    operations = [
        migrations.AddField(
            model_name="recipeingredient",
            name="quantity",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="recipeingredient",
            name="unit",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="recipes.Unit",
            ),
            preserve_default=False,
        ),
    ]
