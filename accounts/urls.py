from .views import (
    CreateUserView,
    ForgotPasswordView,
    LoginRefreshView,
    LogoutUserView,
    RessetPasswordView,
    VerifyAPIView,
    NewVerifyAPIView,
    ChangeUserInformationView,
    ChangeUserPhotoView,
    LoginUserView,
)
from django.urls import path

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('login/refresh/', LoginRefreshView.as_view(), name='login_refresh'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('singup/', CreateUserView.as_view(), name='singup'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
    path('new/verify/', NewVerifyAPIView.as_view(), name='new_verify'),
    path('change/info/', ChangeUserInformationView.as_view(), name='change_info'),
    path('change/photo/', ChangeUserPhotoView.as_view(), name='change_photo'),
    path('forgot/password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('resset/password/', RessetPasswordView.as_view(), name='resset_password'),
]