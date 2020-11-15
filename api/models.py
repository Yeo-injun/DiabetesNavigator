from django.db import models  
from django.contrib.auth.models import User  
from django.db.models.signals import post_save  
from django.dispatch import receiver

class User_Profile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    name =      models.CharField(max_length=64, null=True, verbose_name = '이름')
    sex =       models.BooleanField(null=True, verbose_name = '성별')
    birthday =  models.DateField(null=True, verbose_name = '생년월일') # settings.py 확인 필요
    phone =     models.CharField(max_length=15, null=True, verbose_name = '연락처')

    diabetes_type_CHOICES = (
        ('제1형', 'tyep1_diabetes'),
        ('제2형', 'type2_diabetes'),
        ('임신', 'pregnant_diabetes'),
        ('기타', 'etc'),
    )
    PA_CHOICES = (
        (1.0, '비활동적'),
        (1.12, '저활동적'),
        (1.27, '활동적'),
        (1.45, '매우 활동적'),
    )

    diabetes_type = models.CharField(max_length=10, choices = diabetes_type_CHOICES, null=True, verbose_name= '당뇨병유형' ) # 참고 메소드.. models.TextChoices('A', 'B')
    height =        models.FloatField(max_length=5, null=True, verbose_name= '키' )    
    weight =        models.FloatField(max_length=5, null=True, verbose_name= '몸무게' )
    PA =            models.FloatField(max_length=5, choices = PA_CHOICES, null=True, verbose_name= '신체활동계수') # 참고 메소드.. models.TextChoices('A', 'B')
    energy_needs =  models.FloatField(max_length=5, null=True, verbose_name= '에너지필요량')
    
    class Meta: # 메타 클래스를 이용하여 테이블명 지정
        db_table = 'user_profiles'

# If you've already created some users, you can generate tokens for all existing users like this:
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token

# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)