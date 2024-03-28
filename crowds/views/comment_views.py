from django.contrib import messages # '수정권한이 없습니다' 오류 메세지 발생시키기 위해
from django.contrib.auth.decorators import login_required # @login_required 애더네이션 적용하기
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone # 현재시간 timezone.now() 사용하기 위해

from ..forms import CommentForm
from ..models import Question, Answer, Comment

# 2024.03.20 질문 댓글 등록 함수 추가
@login_required(login_url='common:login') # 2024.03.20 login 먼저하라고!
def comment_create_question(request, question_id):
    """
    crowds 질문 댓글 등록
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST" :
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            comment.author = request.user 
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            # return redirect('crowds:detail', question_id=question.id)
            return redirect('{}#comment_{}'.format(resolve_url('crowds:detail',
                    question_id=comment.question.id), comment.id))
    else :
        form = CommentForm()
    context = {'form': form}
    return render(request, 'crowds/comment_form.html', context)

# 2024.03.20 질문 댓글 수정 함수 추가
@login_required(login_url='common:login') 
def comment_modify_question(request, comment_id):
    """
    crowds 질문 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    # 로그인한 사용자(request.user)와 댓글작성자(comment.author)와 다르면 수정권한없음
    if request.user != comment.author: 
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('crowds:detail', question_id=comment.question.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            comment.author = request.user 
            comment.modify_date = timezone.now() 
            comment.save()
            # return redirect('crowds:detail', question_id=comment.question.id)
            return redirect('{}#comment_{}'.format(resolve_url('crowds:detail',
                    question_id=comment.question.id), comment.id))
    else :
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'crowds/comment_form.html', context)

# 2024.03.20 질문 댓글 삭제 함수 추가
@login_required(login_url='common:login') 
def comment_delete_question(request, comment_id):
    """
    crowds 질문 댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    # 로그인한 사용자(request.user)와 댓글작성자(comment.author)와 다르면 삭제권한없음
    if request.user != comment.author: 
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('crowds:detail', question_id=comment.question.id)
    else :
        comment.delete()
    return redirect('crowds:detail', question_id=comment.question.id)

# 2024.03.20 답변 댓글 등록 함수 추가
@login_required(login_url='common:login') # 2024.03.20 login 먼저하라고!
def comment_create_answer(request, answer_id):
    """
    crowds 답변 댓글 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)

    if request.method == "POST" :
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            comment.author = request.user 
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            # return redirect('crowds:detail', question_id=comment.answer.question.id)
            return redirect('{}#comment_{}'.format(resolve_url('crowds:detail',
                    question_id=comment.answer.question.id), comment.id))
    else :
        form = CommentForm()
    context = {'form': form}
    return render(request, 'crowds/comment_form.html', context)

# 2024.03.20 답변 댓글 수정 함수 추가
@login_required(login_url='common:login') 
def comment_modify_answer(request, comment_id):
    """
    crowds 답변 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    # 로그인한 사용자(request.user)와 댓글작성자(comment.author)와 다르면 수정권한없음
    if request.user != comment.author: 
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('crowds:detail', question_id=comment.question.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            comment.author = request.user 
            comment.modify_date = timezone.now() 
            comment.save()
            # return redirect('crowds:detail', question_id=comment.answer.question.id)
            return redirect('{}#comment_{}'.format(resolve_url('crowds:detail',
                    question_id=comment.answer.question.id), comment.id))
    else :
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'crowds/comment_form.html', context)

# 2024.03.20 답변 댓글 삭제 함수 추가
@login_required(login_url='common:login') 
def comment_delete_answer(request, comment_id):
    """
    crowds 답변 댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    # 로그인한 사용자(request.user)와 댓글작성자(comment.author)와 다르면 삭제권한없음
    if request.user != comment.author: 
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('crowds:detail', question_id=comment.answer.question.id)
    else :
        comment.delete()
    return redirect('crowds:detail', question_id=comment.answer.question.id)