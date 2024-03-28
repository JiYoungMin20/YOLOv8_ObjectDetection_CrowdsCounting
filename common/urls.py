# 2024.03.18 생성

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views # 회원가입 추가할 떄 추가함

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'), # 회원가입
]