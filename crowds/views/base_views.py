from django.core.paginator import Paginator # 2024.03.18 페이징 기능 추가하기
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count # 검색 기능, 정렬 카운트

from ..forms import QuestionForm, AnswerForm
from ..models import Question, Answer

# import logging
# logger = logging.getLogger('crowds')

def index(request) :
    # logger.info("INFO 레벨로 촐력")
    """
    crowds 목록 출력
    """
    # 입력 인자
    page = request.GET.get('page', '1')   # 페이지
    kw = request.GET.get('kw', '')        # 검색
    so = request.GET.get('so', 'recent')  # 정렬 기준
    
    # 정렬
    if so == 'recommend':
      question_list = Question.objects.annotate(
        num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
      question_list = Question.objects.annotate(
        num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else: # recent
      question_list = Question.objects.order_by('-create_date')
    
    # 조회
    # question_list = Question.objects.order_by('-create_date')
    if kw:
      question_list = question_list.filter(
        Q(subject__icontains=kw) |                # 제목 검색
        Q(content__icontains=kw) |                # 내용 검색
        Q(author__username__icontains=kw) |       # 질문 글쓴이 검색
        Q(answer__author__username__icontains=kw) # 답변 글쓴이 검색
      ).distinct()
        
    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    # context = {'question_list': question_list}
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so} # page_obj로 변경, page. kw 추가
    
    return render(request, 'crowds/question_list.html', context) # render 함수 적용
  # return HttpResponse("안녕하세요 crowds에 오신것을 환영합니다. <br/> 오늘도 행복하세요~!")
  
# 2014.03.14 질문상세함수 detail() 추가 
def detail(request, question_id) :
    """
    crowds 내용 출력
    """
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id) # 404 에러 처리 추가
    context = {'question' : question}
    return render(request, 'crowds/question_detail.html', context) 