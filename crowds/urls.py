from django.urls import path
from .views import base_views, question_views, answer_views, comment_views, vote_views

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
    path('question/modify/<int:question_id>/', 
         question_views.question_modify, name='question_modify'), # 질문수정 URL 추가
    path('question/delete/<int:question_id>/', 
         question_views.question_delete, name='question_delete'), # 질문삭제 URL 추가
    
    # answer_views.py
    path('answer/create/<int:question_id>/', 
         answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', 
         answer_views.answer_modify, name='answer_modify'), # 답변수정 URL 추가
    path('answer/delete/<int:answer_id>/', 
         answer_views.answer_delete, name='answer_delete'), # 답변삭제 URL 추가 
    
    # comment_views.py
    
    # 2024.03.20 질문 댓글 (등록,수정,삭제) URL 추가
    path('comment/create/question/<int:question_id>/', 
         comment_views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', 
         comment_views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', 
         comment_views.comment_delete_question, name='comment_delete_question'),
    # 2024.03.20 답변 댓글 (등록,수정,삭제) URL 추가
    path('comment/create/answer/<int:answer_id>/', 
         comment_views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/', 
         comment_views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/', 
         comment_views.comment_delete_answer, name='comment_delete_answer'), 
    
    # vote_view.py
    path('vote/question/<int:question_id>/',
         vote_views.vote_question, name='vote_question'),
    path('vote/answer/<int:answer_id>/',
         vote_views.vote_answer, name='vote_answer'),
]