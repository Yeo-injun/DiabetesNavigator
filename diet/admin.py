from django.contrib import admin
from .models import Meal_record, Food_detail, Food_nutrient

class Meal_record_Admin(admin.ModelAdmin):
    model = Meal_record
    list_display = ('meal_record_ID', 'username', 'time')
admin.site.register(Meal_record, Meal_record_Admin)

class Food_detail_Admin(admin.ModelAdmin):
    model = Food_detail # 같은 값 출력 Code : exclude = (None,)
    list_display = ('pk', 'meal_record_ID', 'food_ID')
admin.site.register(Food_detail, Food_detail_Admin)

class Food_nutrient_Admin(admin.ModelAdmin):
    model = Food_nutrient # 같은 값 출력 Code : exclude = (None,)
    exclude = (None, )
admin.site.register(Food_nutrient, Food_nutrient_Admin)
