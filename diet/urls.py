from django.urls import path

from .views import (Meal_record_ListView, 
                    Meal_record_text_RegisterView,
                    Food_detail_text_RegisterView,
                    Food_detail_ListView,
                    Food_nutrient_ListView,
                    Meal_record_photo_RegisterView,
                    )
# Food_detail = Food_detail_ViewSet.as_view({'get' : 'retrieve'})
# Food_detail = Food_detail_ViewSet.as_view({'get' : 'list'})

urlpatterns = [
    path('list/', Meal_record_ListView.as_view(), name='meal_record_list'),
    path('details/', Food_detail_ListView.as_view(), name='food_detail'), # ?record=<str:meal_record_ID>
    path('meal-text-register/', Meal_record_text_RegisterView.as_view(), name='meal_text_register'),
    path('meal-photo-register/', Meal_record_photo_RegisterView.as_view(), name='meal_photo_register'),
    path('food-list/', Food_nutrient_ListView.as_view(), name='food_list'),
    path('food-text-register/', Food_detail_text_RegisterView.as_view(), name='food_text_register'),
]