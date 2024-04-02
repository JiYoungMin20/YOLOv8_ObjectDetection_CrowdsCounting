from django.urls import path
from .views import base_views, question_views, answer_views

app_name = 'crowds'  # namespace 추가 

urlpatterns = [
     # base_views.py
    path('', 
         base_views.index, name='index'), # 2024.03.13 우아한URL을 위해 name 속성 추가
    path('<int:question_id>/', 
         base_views.detail, name='detail'),
    
    # question_views.py
    path('question/create/', 
         question_views.question_create, name='question_create'), # 질문등록기능 추가
    path('question/delete/<int:question_id>/', 
         question_views.question_delete, name='question_delete'), # 질문삭제 URL 추가
    
    # answer_views.py
    path('answer/create/<int:question_id>/', 
         answer_views.answer_create, name='answer_create'),
    path('answer/delete/<int:answer_id>/', 
         answer_views.answer_delete, name='answer_delete'), # 답변삭제 URL 추가 
]