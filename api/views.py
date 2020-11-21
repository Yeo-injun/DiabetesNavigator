from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from knox.models import AuthToken

from .serializers import Account_Serializer, Profile_Serializer
from .models import User_Profile



#-------- 에너지필요량 계산함수 --------#
def cal_energy_needs(sex, birthdate, PA, weight, height):
    age = datetime.today().year - birthdate.year + 1
    if sex == True : # 남자일때 energy_needs 계산
        male_energy_needs = 354 - (6.91 * age) + PA*(9.36*weight + 726*height)
        return male_energy_needs
    else : 
        female_energy_needs = 662 - (9.53 * age) + PA*(15.91*weight + 539.6*height)
        return female_energy_needs


# Account_Register API
class Account_RegisterAPI(generics.GenericAPIView):
    serializer_class = Account_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        create_token = AuthToken.objects.create(user)
        
        return Response({
        "user": Account_Serializer(user, context=self.get_serializer_context()).data,
        "token": create_token[1]
        })


# Profile_Register API // 에너지 필요량 프론트엔드에서 계산해서 받기..
class ProfileAPI(generics.GenericAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = User_Profile.objects.all()
    serializer_class = Profile_Serializer

    # 프로필 조회
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.get(user = request.user)
        # queryset = queryset.get(user = 4)

        serializer = self.get_serializer_class()
        serializer = serializer(queryset)

        return Response(serializer.data)

    # 프로필 등록 // energy_needs는 프론트에서 계산해서 넘겨주기...
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True) 
        profile = serializer.save()
        
        return Response({
        "profile": Profile_Serializer(profile, context=self.get_serializer_context()).data,
        })

#-------------------------------------------------------------------------------------------------#
# login 기능 구현 // logout 기능은 urls.py에서 처리
from django.contrib.auth import login 
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView



class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    
    @method_decorator(ensure_csrf_cookie)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
