from django import forms
from crowds.models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content', 'upload_image']

        labels = { # label 속성 수정. 한글로 바꾸자
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
