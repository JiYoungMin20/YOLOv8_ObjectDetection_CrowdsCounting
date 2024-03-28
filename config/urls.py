"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # include 추가
from crowds.views import base_views # 기존의 views.py 파일을 views 폴더를 만들어 분리함
from django.conf.urls.static import static # 이미지 등 static 관련
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crowds/', include('crowds.urls')), # 2024.03.27 밀집도분석app 추가
    path('common/', include('common.urls')), # common/urls.py 파일로 유도
    path('', base_views.index, name='index'), # '/'에 해당하는 path. views 대신에 base_views 로 변경
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # media 경로 추가

