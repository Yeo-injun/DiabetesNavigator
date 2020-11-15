from rest_framework import serializers
from django.contrib.auth.models import User

from .models import User_Profile

class Account_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class Profile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Profile
        fields = ('user', 'name', 'sex', 'birthday', 'phone', 
        'diabetes_type', 'height', 'weight', 'PA', 'energy_needs') # energy_needs는 BackEnd에서 계산해서 Response

#----------------------------------------------------------------#

from diet.models import Meal_record, Food_detail, Food_nutrient

class Meal_record_ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal_record
        fields = ('username', 'meal_record_ID', 'date', 'time', 'photo_file')


class Meal_record_text_RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal_record
        fields = ('username', 'meal_record_ID', 'date', 'time')


class Food_detail_text_RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food_detail
        fields = ('meal_record_ID', 'food_ID', 'food_name', 'food_quantity')


class Food_detail_ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food_detail
        fields = ('meal_record_ID', 'food_ID', 'food_name', 
                'food_quantity', 'food_kcal', 'carbohydrate_intake', 'protein_intake', 'fat_intake')


class Food_nutrient_ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food_nutrient
        fields = ('food_ID', 'food_name')
#----------------------------------------------------------------#
