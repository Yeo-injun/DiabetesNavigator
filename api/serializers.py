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
from rest_framework.validators import UniqueValidator

class Meal_record_Serializer(serializers.Serializer):
    meal_record_ID = serializers.CharField(label='식사기록아이디', max_length=10, read_only=True) # validators=[UniqueValidator(queryset=Meal_record.objects.all())])
    date = serializers.DateField(label='입력날짜', required=False)
    time = serializers.DateTimeField(label='입력시간', required=False)
    photo_file = serializers.ImageField(allow_null=True, max_length=100, required=False)
    ## meal_record내 음식 영양성분별 총계 Field
    kcal_total = serializers.IntegerField(label='총 칼로리')
    carbohydrate_total = serializers.IntegerField(label='총 탄수화물')
    protein_total = serializers.IntegerField(label='총 단백질')
    fat_total = serializers.IntegerField(label='총 지방')

class Meal_record_ListSerializer(serializers.Serializer):
    # index = serializers.CharField(label='게시글 인덱스', max_length=10, read_only=True)
    record_list = Meal_record_Serializer(many=True)
    
    # class Meta:
    #     extra_kwargs = {'record_list': {'required': False}}

# class Meal_record_ListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Meal_record
#         fields = ('username', 'meal_record_ID', 'date', 'time', 'photo_file')


class Meal_record_text_RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal_record
        fields = ('username', 'meal_record_ID', 'date', 'time')


class Meal_record_photo_RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal_record
        # fields = ('username', 'date', 'time', 'photo_file', 'photo_name')
        fields = ('username', 'meal_record_ID', 'date', 'time', 'photo_origin', 'photo_yolo', 'photo_name')


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
