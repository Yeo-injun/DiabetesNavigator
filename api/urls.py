from knox import views as knox_views

from django.urls import path

from .views import (Account_RegisterAPI, 
                    Profile_RegisterAPI,
                    LoginAPI,
                    )

urlpatterns = [
    path('account-register/', Account_RegisterAPI.as_view(), name='account-register'),
    path('profile-register/', Profile_RegisterAPI.as_view(), name='profile-register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]