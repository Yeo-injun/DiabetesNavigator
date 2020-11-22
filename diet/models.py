from django.db import models
from django.contrib.auth.models import User  
from datetime import date
from django.utils import timezone

from api.models import User_Profile

class Meal_record(models.Model): # 식사기록 테이블
    meal_record_ID =    models.CharField(primary_key=True, max_length=10, verbose_name='식사기록아이디')
    username =          models.ForeignKey(User, on_delete=models.CASCADE, db_column= '사용자아이디')
    date =              models.DateField(verbose_name='입력날짜', default=date.today) # Python의 datetime.date인스턴스로 '날짜'
    time =              models.DateTimeField(verbose_name='입력시간', default=timezone.now) # Python의 datetime.datetime 인스턴스로 '날짜'와 '시간'
    photo_origin =      models.ImageField(upload_to='photos', blank=True, null=True) # 파일경로 재설정
    photo_yolo =        models.ImageField(upload_to='photos/yolo', blank=True, null=True)
    photo_name =        models.CharField(max_length=100, verbose_name='사진이름', blank=True, null=True)

    class Meta: # 메타 클래스를 이용하여 테이블명 지정
        db_table = 'meal_record'

class Food_detail(models.Model): # 식사기록 세부정보 테이블
    meal_record_ID =        models.ForeignKey(Meal_record, on_delete=models.CASCADE, db_column= 'meal_record_ID')
    food_ID =               models.CharField(max_length=10, verbose_name='음식아이디')              
    food_name =             models.CharField(max_length=50, verbose_name='음식명')
    food_quantity =         models.IntegerField(verbose_name='음식양')
    food_kcal =             models.IntegerField(verbose_name='음식열량')
    carbohydrate_intake =   models.IntegerField(verbose_name='탄수화물섭취량')
    protein_intake =        models.IntegerField(verbose_name='단백질섭취량')
    fat_intake =            models.IntegerField(verbose_name='지방섭취량')

    class Meta: # 메타 클래스를 이용하여 테이블명 지정
        db_table = 'food_details'

class Food_nutrient(models.Model) :
    food_ID =   	models.CharField(primary_key=True, max_length=10, verbose_name = '음식ID')
    food_name = 	models.CharField(max_length=50, verbose_name='음식명')
    one_serving	=   models.IntegerField(verbose_name='1인분')
    kcal =      	models.IntegerField(verbose_name='열량')
    carbohydrate =  models.IntegerField(verbose_name='탄수화물')
    protein	=       models.IntegerField(verbose_name='단백질')
    fat =           models.IntegerField(verbose_name='지방')

    class Meta: # 메타 클래스를 이용하여 테이블명 지정
        db_table = 'food_nutrients'