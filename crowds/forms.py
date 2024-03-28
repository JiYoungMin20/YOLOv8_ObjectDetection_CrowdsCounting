from django import forms
from crowds.models import Question, Answer, Comment

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content', 'upload_image']

        """ 
        forms.as_p 자동 생성하는 부분을 수작업으로 폼 작성하기 위해 주석 처리
        
        widgets = {  # 폼에 부트스트랩 css 적용하기
            'subject' : forms.TextInput(attrs={'class': 'form-control'}),
            'content' : forms.Textarea(attrs={'class': 'form-control', 'rows':4}),
        }
        """

        labels = { # label 속성 수정. Subject,COntent로 한글로 바꾸자
            'subject': '제목',
            'content': '내용',
            'upload_image': '제보이미지'
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'predicted_image']
        labels = {
            'content': '답변내용',
            'predicted_image': '분석이미지'
        }

# 2024.03.20 질문 댓글 폼 작성
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }