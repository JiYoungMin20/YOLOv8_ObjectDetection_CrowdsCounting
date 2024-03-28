from django.contrib import admin
from .models import Question 

# Register your models here.

class QuestionAdmin(admin.ModelAdmin): # 장고Admin에 데이터 검색기능추가하기
    search_fields = ['subject']

# admin.site.register(Question) # admin에서 관리 가능하도록 추가
admin.site.register(Question, QuestionAdmin) # class 내용으로 변경
