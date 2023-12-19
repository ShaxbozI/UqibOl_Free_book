from django.shortcuts import render
from .models import VIA_EMAIL, VIA_PHONE, User
from .serializers import (
    ForgotPasswordSerializer,
    LoginRefreshSerializer,
    LoginUserSerializer,
    LogoutSerializer,
    RessetPaswordSerializer,
    SignUpSerializer,
    ChangeUserInformation, 
    ChangeUserPhoto,
)
from utility.utility import send_email, check_email_or_phone 

from django.core.exceptions import ObjectDoesNotExist
from django.utils.datetime_safe import datetime
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = SignUpSerializer
    
    
    

class VerifyAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        user = self.request.user       # user ->
        code = self.request.data.get('code') # 4083

        self.check_verify(user, code)
        return Response(
            data={
                "success": True,
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token']
            }
        )

    @staticmethod
    def check_verify(user, code):       # 12:03 -> 12:05 => expiration_time=12:05   12:04
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        print(verifies)
        if not verifies.exists():
            data = {
                "message": "Tasdiqlash kodingiz xato yoki eskirgan"
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
        return True


    def get(self, request, *args, **kwargs):
        user = self.request.user             # user ->

        self.check_verify_new(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_email(user.phone, code)
        else:
            data = {
                "message": "Email yoki telefon taqami noto'g'ri"
            }
            raise ValidationError(data)
        
        return Response(
            {
                "success": True,
                "message": "Tasdiqlash kodi qayta yuborildi"
            }
        )
        
    @staticmethod
    def check_verify_new(user):       # 12:03 -> 12:05 => expiration_time=12:05   12:04
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                "message": "Tasdiqlash kodining amal qilish vaqti tugamadi"
            }
            raise ValidationError(data)
        
        


class NewVerifyAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user             # user ->

        self.check_verify_new(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_email(user.phone, code)
        else: 
            data = {
                "message": "telfon raqammi yoki email xato",
            }
            
        return Response(
            data={
                "success": True,
                "message": "Yangi tasdiqlash kodi yuborildi",
            }
        )

    @staticmethod
    def check_verify_new(user):       # 12:03 -> 12:05 => expiration_time=12:05   12:04
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                "message": "Tasdiqlash kodining amal qilish vaqti tugamadi biroz kuting"
            }
            raise ValidationError(data)
        
        
  
        
class ChangeUserInformationView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChangeUserInformation
    http_method_names = ['putch', 'put'] 
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        super(ChangeUserInformationView, self).update(request, *args, **kwargs)
        data = {
            "success": True,
            "message": "Foydalanuvchi muvofaqiyatli yaratildi",
        }
        return Response(data, status=200)
        
    def partial_update(self, request, *args, **kwargs):
        super(ChangeUserInformationView, self).partial_update(request, *args, **kwargs)
        data = {
            'success': True,
            "message": "User updated successfully",
        }
        return Response(data, status=200)




class ChangeUserPhotoView(APIView):
    permission_classes = [IsAuthenticated, ]

    def put(self, request, *args, **kwargs):
        serializer = ChangeUserPhoto(data = request.data)
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response({
                "message": "Rasm muvofaqiyatli qo'shildi"
            }, status = 200)
        return Response(
            serializer.errors, status = 400
        )




class LoginUserView(TokenObtainPairView):
    serializer_class = LoginUserSerializer
    
    
   
    
class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer
    



class LogoutUserView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated, ]
    
    # post metodi orqali kelgan malumotdan refresh tokenni olamiz va uni blacklistga oylaymiz
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = self.request.data)
        serializer.is_valid(raise_exception = True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                'success': True,
                'message': 'Siz saytdan chiqdingiz'
            }
            return Response(data, status = 205)
        except TokenError:
            return Response(status = 400)
        
        
   
        
class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny, ]
    
    def post(self, request,  *args, **kwargs):
        serializer = self.serializer_class(data = self.request.data)
        serializer.is_valid(raise_exception = True)
        email_or_phone = serializer.validated_data.get('email_or_phone')
        user = serializer.validated_data.get('user')
        if check_email_or_phone(email_or_phone) == 'phone':
            code = user.create_verify_code(VIA_PHONE)
            send_email(email_or_phone, code)
        
        if check_email_or_phone(email_or_phone) == 'email':
            code = user.create_verify_code(VIA_EMAIL)
            send_email(email_or_phone, code)
            
        return Response(
            {
                'success': True,
                'message': 'Tasdiqlash kodi yuborildi',
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token'],
            }, status = 200
        )
            
            
      
            
class RessetPasswordView(UpdateAPIView):
    serializer_class = RessetPaswordSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['pacht', 'put']
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        response =super(RessetPasswordView, self).update(request, *args, **kwargs)
        try: 
            user = User.objects.get(id = response.data.get('id'))
        except ObjectDoesNotExist as e:
            raise NotFound(detail = 'Foydalanuvchi topilmadi')
        return Response(
            {
                'success': True,
                'message': 'Parolingiz muvofaqiyatli almashtirildi',
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token'],
            }
        )