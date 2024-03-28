from django.db import models
from django.contrib.auth.models import User # 2024.03.19 author 필드 추가하기 위해

# 2024.03.14 추가
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_question') # 글쓴이 추가. related_name 추가
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True) # 수정일자 추가
    voter = models.ManyToManyField(User, related_name='voter_question') # voter추가. related_name 추가
    upload_image = models.ImageField(upload_to="question/%Y%m%d", null=True, blank=True) # 제보이미지
    
    def __str__(self):
        return self.subject

# 2024.03.14 추가
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_answer') # 글쓴이 추가. related_name 추가
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True) # 수정일자 추가
    voter = models.ManyToManyField(User, related_name='voter_answer') # voter추가. related_name 추가
    predicted_image = models.ImageField(upload_to="", null=True, blank=True) # 분석이미지
    
#2024.03.20 댓글 기능 추가하기
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, 
                                 on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True,
                               on_delete=models.CASCADE)