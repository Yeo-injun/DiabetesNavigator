from rest_framework import generics, permissions
from rest_framework.response import Response

from knox.models import AuthToken

from .serializers import Account_Serializer, Profile_Serializer

# Account_Register API
class Account_RegisterAPI(generics.GenericAPIView):
    serializer_class = Account_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True) :
            user = serializer.save()
            return Response({
            "user": Account_Serializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
            })

# Profile_Register API
class Profile_RegisterAPI(generics.GenericAPIView):
    serializer_class = Profile_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True) :
            profile = serializer.save()
            return Response({
            "profile": Profile_Serializer(profile, context=self.get_serializer_context()).data,
            })

#-------------------------------------------------------------------------------------------------#
# login 기능 구현 // logout 기능은 urls.py에서 처리
from django.contrib.auth import login 

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid(raise_exception=True): # serialize된 data가 invalid하면 오류 메세지가 뜸
            user = serializer.validated_data['user']
            login(request, user)
            return super(LoginAPI, self).post(request, format=None)