from django.db import models
from django.contrib.auth.models import User 

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_question') # 글쓴이 추가. related_name 추가
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    upload_image = models.ImageField(upload_to="question/%Y%m%d", null=True, blank=True) # 제보이미지
    
    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_answer') # 글쓴이 추가. related_name 추가
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    predicted_image = models.ImageField(upload_to="", null=True, blank=True) # 분석이미지
    