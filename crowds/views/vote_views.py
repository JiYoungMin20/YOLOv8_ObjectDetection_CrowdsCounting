from django.contrib import messages # '수정권한이 없습니다' 오류 메세지 발생시키기 위해
from django.contrib.auth.decorators import login_required # @login_required 애더네이션 적용하기
from django.shortcuts import get_object_or_404, redirect 

from ..models import Question, Answer

# 2024.03.20 질문추천등록 vote_question() 함수 추가
@login_required(login_url='common:login') # login 먼저하라고!
def vote_question(request, question_id):
    """
    crowds 질문 추천 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author: # 추천자와 글쓴이가 동일하면 안되요.
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        question.voter.add(request.user) # 같은 사용자가 여러번 추천해도 추천수 증가하지 않음
    return redirect('crowds:detail', question_id=question.id)

# 2024.03.20 답변추천등록 vote_answer() 함수 추가
@login_required(login_url='common:login') # login 먼저하라고!
def vote_answer(request, answer_id):
    """
    crowds 답변 추천 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author: # 추천자와 글쓴이가 동일하면 안되요.
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        answer.voter.add(request.user) # 같은 사용자가 여러번 추천해도 추천수 증가하지 않음
    return redirect('crowds:detail', question_id=answer.question.id)