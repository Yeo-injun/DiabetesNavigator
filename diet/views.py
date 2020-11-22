from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from knox.models import AuthToken

from .models import Meal_record, Food_detail, User
from api.serializers import (Meal_record_ListSerializer, 
                            Meal_record_Serializer,
                            Meal_record_text_RegisterSerializer,
                            Food_detail_text_RegisterSerializer,
                            Food_detail_ListSerializer,
                            Food_nutrient_ListSerializer,
                            )  

### 식단 목록 조회 ###
class Meal_record_ListView(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Meal_record.objects.all()
    serializer_class = Meal_record_ListSerializer

    def list(self, request):
        # Meal_record에 있는 모든 인스턴스를 QuerySet으로 가져온다.
        queryset = self.get_queryset() 

        # QuerySet에서 로그인한 유저에 해당하는 데이터만 추출한다. 
        queryset = queryset.filter(username=request.user)

        # queryset[인덱스]에서 meal_record_ID 추출해서 food_detail 필터링
        print("****************************************queryset")
        record_len = len(queryset)
        record_dict = dict()
        record_list = list()

        # 반복문을 통해 모든 식단의 영양성분 총합 구하기
        for idx in range(0, record_len):
            meal_record_ID = queryset[idx].meal_record_ID
            date = queryset[idx].date
            time = queryset[idx].time
            photo_yolo = queryset[idx].photo_yolo
            print(photo_yolo)
            print(meal_record_ID)

            kcal_total = 0
            carbohydrate_total = 0
            protein_total = 0
            fat_total = 0

            # 식단 1개의 음식 영양성분 총합 구하기  
            if meal_record_ID is not None :
                Food_detail_queryset = Food_detail.objects.filter(meal_record_ID = meal_record_ID)  
                
                for cnt in range(0, len(Food_detail_queryset)):
                    kcal_total += Food_detail_queryset[cnt].food_kcal
                    carbohydrate_total += Food_detail_queryset[cnt].carbohydrate_intake
                    protein_total += Food_detail_queryset[cnt].protein_intake
                    fat_total += Food_detail_queryset[cnt].fat_intake               
                print(kcal_total, carbohydrate_total, protein_total, fat_total)
                
                print("#################################### 과연두둥")
                # 음식별 영양성분 총합 데이터 추가하여 Dict객체 만들기
                meal_record_dict = {}
                meal_record_dict['meal_record_ID'] = meal_record_ID
                meal_record_dict['date'] = date
                meal_record_dict['time'] = time
                # meal_record_dict['photo_yolo'] = photo_yolo  (아마 이미지 필드로 반영해야할듯...)Error!! : The 'photo_yolo' attribute has no file associated with it.
                meal_record_dict['kcal_total'] = kcal_total
                meal_record_dict['carbohydrate_total'] = carbohydrate_total
                meal_record_dict['protein_total'] = protein_total
                meal_record_dict['fat_total'] = fat_total
                
                # record_list에 추가하기
                record_list.append(meal_record_dict)
        
        # 페이지 지정 // 오류 확인...!
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        record_dict['record_list'] = record_list
        return Response(record_dict)  # Respone시에 dict형태면 Serialize 해주지 않아도 됨!


#----------------------------------------------------------------#

### 식단 등록(Text) - 식단 객체 생성 ###
class Meal_record_text_RegisterView(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated] 

    serializer_class = Meal_record_text_RegisterSerializer

    def post(self, request, *args, **kwargs) :
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True) :
            meal_record = serializer.save()
            return Response({"meal_record" : Meal_record_text_RegisterSerializer(meal_record, context=self.get_serializer_context()).data})

#----------------------------------------------------------------#

### 식단 등록(Text) - DB에 저장된 음식목록(영양성분) 가져오기 ###
from .models import Food_nutrient

class Food_nutrient_ListView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated] // 권한에 상관없이 접근

    queryset = Food_nutrient.objects.all()
    serializer_class = Food_nutrient_ListSerializer

    def get(self, request, *args, **kwargs) :
        # 음식영양성분 테이블에 저장된 모든 레코드 인스턴스로 가져오기
        queryset = self.get_queryset()

        # 자료구조가 QuerySet인 인스턴스를 Serializer로 직렬화
        serializer = self.serializer_class(queryset, many = True)
        
        # 해당 데이터를 .data 부분만 Response
        return Response(serializer.data)

#----------------------------------------------------------------#

### 식사 등록(Text) - DB저장된 음식목록에서 음식선택해서 등록하기 ###
from .models import Food_nutrient

# food_nutrient 테이블에서 음식영양소 조회
def retrieve_food(food_ID):
    queryset = Food_nutrient.objects.get(food_ID = food_ID) # QuerySet으로 DB Objects 추출(속성, 메소드 존재)
    food_name = queryset.food_name
    one_serving = queryset.one_serving
    kcal = queryset.kcal 
    carbohydrate = queryset.carbohydrate 
    protein = queryset.protein
    fat = queryset.fat
    return food_name, one_serving, kcal, carbohydrate, protein, fat # food_name은 이후 수정시에 추가예정

class Food_detail_text_RegisterView(generics.GenericAPIView):
    serializer_class = Food_detail_text_RegisterSerializer
    permission_classes = [IsAuthenticated] 
    
    def post(self, request, *args, **kwargs) :
        serializer = self.get_serializer(data=request.data) # request.data => Querydic

        if serializer.is_valid(raise_exception=True) :
            # Serializer에서 음식ID 등 value값 추출
            meal_record_ID = serializer.data['meal_record_ID']
            food_ID = serializer.data['food_ID']
            # food_name = serializer.data['food_name'] ### 너는 탈락이야 임마!!
            food_quantity = serializer.data['food_quantity']

            # 음식ID로 음식영양성분 DB조회 : 음식량에 따른 영양성분 계산을위해 1인분기준 영양성분 변수 할당
            # food_nutrient = Food_nutrient.objects.get(food_ID = food_ID) # QuerySet으로 DB Objects 추출(속성, 메소드 존재)
            food_name, one_serving, kcal, carbohydrate, protein, fat = retrieve_food(food_ID)
            
            # 음식양에 따라 섭취량 계산
            food_kcal = food_quantity * (kcal / one_serving) 
            carbohydrate_intake = food_quantity * (carbohydrate / one_serving) 
            protein_intake = food_quantity * (protein / one_serving)
            fat_intake = food_quantity * (fat / one_serving)

            # 데이터를 저장할 DB객체 생성 
            # 외래키 필드로 정의된 것은 인스턴스(객체)로 변수에 할당해주어야 함
            meal_record = Meal_record.objects.get(meal_record_ID = meal_record_ID)
            
            # 모델 인스턴스 DB에 저장
            food_detail = Food_detail.objects.create(
                        meal_record_ID = meal_record,
                        food_ID = food_ID,
                        food_name = food_name,
                        food_quantity = food_quantity,
                        food_kcal = food_kcal, 
                        carbohydrate_intake = carbohydrate_intake, 
                        protein_intake = protein_intake, 
                        fat_intake = fat_intake
                        )

            # DB에 저장된 모델 인스턴스 Return
            return Response({"food_detail" 
                            : Food_detail_ListSerializer(food_detail, context=self.get_serializer_context()).data})

#----------------------------------------------------------------#

# ### 식사 등록(Photo) - YOLO 객체 인식 결과값 반환###
# from api.serializers import Meal_record_photo_RegisterSerializer
# import subprocess
# import os

# class Meal_record_photo_RegisterView(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]

#     serializer_class = Meal_record_photo_RegisterSerializer

#     def post(self, request, *args, **kwargs) :
#         # 클라이언트가 보낸 원본사진 변수에 할당
#         photo = request.data['photo_file'] # 사진 경로 확인 필요...


#         # 원본사진 YOLO로 보낸 후 YOLO 실행

       
#         # photo 변수를 넣어서 Yolo 실행 
#         # 실행 결과값 return받아서 yolo_photo 변수에 저장


#         # YOLO 객체인식 결과값을 영양성분 조회를 위해 list로 만들기


#         # YOLO Return값을 반영하여 Serialize 하기 
#         # Serialize된 데이터 DB에 저장
#         temp = {'username':request.data['username'],
#                 'meal_record_ID':request.data['meal_record_ID'],
#                 'date':request.data['date'],
#                 'time':request.data['time'],
#                 'photo_file': photo 
#                 # 'photo_name':"테스트용"
#                 }
#         serializer = self.get_serializer(data=temp)
#         serializer.is_valid(raise_exception=True)
#         meal_record = serializer.save()

#         # 식단기록(Meal_record)에 음식영양성분(Food_detail) 등록하기
#         # if not yolo_food_list :
#         #     error = {"error" : "None exist!"}
#         # else : 
#         #     for food_ID in yolo_food_list :
#         #         food_name, one_serving, kcal, carbohydrate, protein, fat = retrieve_food(food_ID)
#         #         food_detail = Food_detail.objects.create(
#         #                         meal_record_ID = Meal_record.objects.get(meal_record_ID = request.data['meal_record_ID']),
#         #                         food_ID = food_ID,
#         #                         food_name = food_name,
#         #                         food_quantity = one_serving,
#         #                         food_kcal = kcal, 
#         #                         carbohydrate_intake = carbohydrate, 
#         #                         protein_intake = protein, 
#         #                         fat_intake = fat
#         #                         )

#         # 등록된 식단기록 데이터 Return  -> 수정방향 : 해당 식단기록에 등록된 음식성분까지 보여주기(YOLO인식 사진 + 객체인식된 음식영양정보)
#         return Response({"meal_record" : Meal_record_text_RegisterSerializer(meal_record, context=self.get_serializer_context()).data})

#----------------------------------------------------------------#

### 식사기록 섭취음식 조회 ###
class Food_detail_ListView(generics.GenericAPIView):
    queryset = Food_detail.objects.all()
    serializer_class = Food_detail_ListSerializer

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # 식사기록 아이디 추출 : URL에 쿼리문 작성하여 GET방식으로 넘긴 데이터 중에 value값만 추출
        record_ID = request.GET['record']
        
        # QuerySet 객체 생성
        queryset_get = self.get_queryset()
        
        # QuerySet 필터링 : 하나의 식사기록에 포함돼 있는 음식세부정보 필터링
        record_by_ID = queryset_get.filter(meal_record_ID = record_ID)

        # Serializer 객체 생성
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(record_by_ID, many=True, context={'request': request})
        
        return Response(serializer.data)



### 식사 등록(Photo) - YOLO 객체 인식 결과값 반환###
from api.serializers import Meal_record_photo_RegisterSerializer
import subprocess
import os

class Meal_record_photo_RegisterView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = Meal_record_photo_RegisterSerializer

    def post(self, request, *args, **kwargs) :
        # 클라이언트가 보낸 원본사진 DB저장
        photo_origin = request.data['photo_origin'] # 사진 경로 확인 필요...
        before_yolo = {'username':request.data['username'],
                        'meal_record_ID':request.data['meal_record_ID'],
                        'date':request.data['date'],
                        'time':request.data['time'],
                        'photo_origin' : photo_origin
                        }
        
        serializer = self.get_serializer(data=before_yolo)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("오류뜨는가?? 제목만 출력하고 싶다구!!")
        print(type(photo_origin))
        print("2번째 관문~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print()

        # 원본사진 YOLO로 보낸 후 YOLO 실행
        # YOLO 실행 준비 :  대상 이미지 경로 설정 / 객체 인식 결과를 text파일로 반환 
        print('########## 정상 실행될 것이다?!')
        exe_yolo = '/home/allrecipes/project/yolo/darknet/darknet detector test /home/allrecipes/project/yolo/darknet/custom_data/detector.data /home/allrecipes/project/yolo/darknet/custom_data/cfg/yolov3-custom.cfg /home/allrecipes/project/yolo/darknet/backup/yolov3-custom_final.weights '
        saved_photo_path = '/home/allrecipes/project/django/DiabetesNavigator/photos/ '
        saved_photo_name = str(photo_origin)
        yolo_text = saved_photo_name[:-4] + '.txt'
        
        # ubuntu 실행 명령 실행
        os.system(exe_yolo + saved_photo_path + saved_photo_name + '> ./yolo_result/' + yolo_text)
        print('########## 정상 실행되었다?!')

        # YOLO 객체인식 결과값을 영양성분 조회를 위해 list로 만들기
        yolo_text = "/home/allrecipes/project/django/DiabetesNavigator/yolo_result/" + yolo_text #/yolo_result 디렉토리 추가
        yolo_food_list = []

        f = open(yolo_text)
        header = f.readline() # 첫번째 줄을 읽는다. 해당 파일의 첫줄은 의미 X
        for line in f : # 두번째 줄 이후부터 Text 추출
            line = line.split(":")
            food = line[0]
            yolo_food_list.append(food)
        f.close()        
        print(yolo_food_list)

        # YOLO 객체인식 결과 이미지 DB저장
        after_yolo = Meal_record.objects.get(meal_record_ID=meal_record_ID)
        after_yolo.update(photo_yolo=photo_yolo) # photo_yolo에 YOLO 객체인식 이미지 할당하기

        # 식단기록(Meal_record)에 음식영양성분(Food_detail) 등록하기
        if not yolo_food_list :
            error = {"error" : "None exist!"}
        else : 
            for food_ID in yolo_food_list :
                food_name, one_serving, kcal, carbohydrate, protein, fat = retrieve_food(food_ID)
                # 식단기록내 음식생성
                food_detail = Food_detail.objects.create(
                                meal_record_ID = Meal_record.objects.get(meal_record_ID = request.data['meal_record_ID']),
                                food_ID = food_ID,
                                food_name = food_name,
                                food_quantity = one_serving,
                                food_kcal = kcal, 
                                carbohydrate_intake = carbohydrate, 
                                protein_intake = protein, 
                                fat_intake = fat
                                )

        # 등록된 식단기록 데이터 Return  -> 수정방향 : 해당 식단기록에 등록된 음식성분까지 보여주기(YOLO인식 사진 + 객체인식된 음식영양정보)
######### 테스트 필요.... ##########
        return Response({"meal_record" : Meal_record_photo_RegisterSerializer(data=after_yolo, context=self.get_serializer_context()).data,
                        "details" : Food_detail_ListSerializer(data=Food_detail.objects.filter(meal_reacord_ID=meal_record_ID)).data})

