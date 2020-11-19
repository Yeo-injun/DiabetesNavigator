from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from knox.models import AuthToken

from .models import Meal_record, Food_detail
from api.serializers import (Meal_record_ListSerializer, 
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

        # Meal_record Serializer 객체 생성하고 QuerySet으로 받은 데이터를 넘겨준다.
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        # 페이지 지정
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

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

### 식단 등록(Text) - DB에 저장된 음식목록 가져오기 ###
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
        serializer = self.get_serializer(data=request.data)

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

### 식사 등록(Photo) - YOLO 객체 인식 결과값 반환###
from api.serializers import Meal_record_photo_RegisterSerializer
import subprocess

class Meal_record_photo_RegisterView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = Meal_record_photo_RegisterSerializer

    def post(self, request, *args, **kwargs) :
        # 클라이언트가 보낸 원본사진 변수에 할당
        photo = request.data['photo_file'] # 사진 경로 확인 필요...

        # 원본사진 YOLO로 보낸 후 YOLO 실행
        ##########################################
        print('########## 정상 실행될 것이다?!')
        path = "/home/allrecipes/project/yolo/darknet"
        yolo_photo, yolo_text = subprocess.check_output(
            path + "/darknet detector test custom_data/detector.data custom_data/cfg/yolov3-custom.cfg backup/yolov3-custom_final.weights ./" 
            + photo + ' > ' + photo + ".txt") # YOLO 실행 명령어 및 반환 변수 설정
        print('########## 정상 실행되었다?!')
        # photo 변수를 넣어서 Yolo 실행 
        # 실행 결과값 return받아서 yolo_photo 변수에 저장
        ##########################################

        # YOLO Return값 변수에 저장
        # yolo_text = "" # text 파일 read 필요... / models.py에서 파일 필드로 수정??...
        # yolo_food_list = "" # yolo_text 파일을 read해서 food_ID 추출

        # YOLO Return값을 반영하여 Serialize 하기 
        # Serialize된 데이터 DB에 저장
        temp = {'username':request.data['username'],
                'meal_record_ID':request.data['meal_record_ID'],
                'date':request.data['date'],
                'time':request.data['time'],
                'photo_file': yolo_photo,
                'photo_name':"테스트용"
                }
        serializer = self.get_serializer(data=temp)
        if serializer.is_valid(raise_exception=True) :
            meal_record = serializer.save()

        # 식단기록(Meal_record)에 음식영양성분(Food_detail) 등록하기
        # if not yolo_food_list :
        #     error = {"error" : "None exist!"}
        # else : 
        #     for food_ID in yolo_food_list :
        #         food_name, one_serving, kcal, carbohydrate, protein, fat = retrieve_food(food_ID)
        #         food_detail = Food_detail.objects.create(
        #                         meal_record_ID = request.data['meal_record_ID'],
        #                         food_ID = food_ID,
        #                         food_name = food_name,
        #                         food_quantity = one_serving,
        #                         food_kcal = kcal, 
        #                         carbohydrate_intake = carbohydrate, 
        #                         protein_intake = protein, 
        #                         fat_intake = fat
        #                         )

        # 등록된 식단기록 데이터 Return  -> 수정방향 : 해당 식단기록에 등록된 음식성분까지 보여주기(YOLO인식 사진 + 객체인식된 음식영양정보)
        return Response({"meal_record" : Meal_record_text_RegisterSerializer(meal_record, context=self.get_serializer_context()).data})

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













########################################################

# class Meal_record_details_View(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Meal_record_details.objects.all()
#     serializer_class = Meal_record_details_Serializer
#     permission_classes = [IsAuthenticated]
#     print('+++++++++++++++++++++++++++')
#     lookup_field = 'meal_record_ID'
#     print('@@@@@@@@@@@@@@@@@@@@@@@@@@')


#     def get(self, request, *args, **kwargs):
#         # queryset = self.filter_queryset(meal_record_ID = args)
        
#         print(self.lookup_field)
#         # print(queryset)
#         print(request.user)
#         print('+++++++++++++++++++++++++++++++')
#         # queryset = queryset.filter(meal_record_details = )
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)



# ##############################################
# from rest_framework.views import APIView

# class Meal_record_details_View(APIView):
#     authentication_classes = (SessionAuthentication, BasicAuthentication)
#     permission_classes = (IsAuthenticated,)
#     # 속성(property) 생성
#     queryset = Meal_record_details.objects.all()
#     serializer_class = Meal_record_list_Serializer

#     def get(self, request, meal_record_ID):
#         # Meal_record에 있는 모든 인스턴스를 QuerySet으로 가져온다.
#         queryset = self.filter(meal_record_ID = meal_record_ID)
#         print('게시글 하나 가져오기 ###############')
        
#         serializer_class = self.get_serializer_class()
#         print(type(serializer_class.data))
#         serializer = serializer_class(queryset, many=True)
#         print(serializer)
#         print('###############')
#         return Response(serializer.data)

    # get_object()  세부 항목으로 사용될 객체 instance를 반환
    
    # def get_object(self):
    #     queryset = self.get_queryset()
    #     filter = {}
    #     for field in self.multiple_lookup_fields:
    #         filter[field] = self.kwargs[field]

    #     obj = get_object_or_404(queryset, **filter)
    #     self.check_object_permissions(self.request, obj)
    #     return obj
    pass