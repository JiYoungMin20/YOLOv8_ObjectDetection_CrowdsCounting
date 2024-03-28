from django.contrib import messages # '수정권한이 없습니다' 오류 메세지 발생시키기 위해
from django.contrib.auth.decorators import login_required # @login_required 애더네이션 적용하기
from django.shortcuts import render, get_object_or_404, redirect 
from django.utils import timezone # 현재시간 timezone.now() 사용하기 위해

from ..forms import QuestionForm
from ..models import Question
from .answer_views import *  # 답변 자동 생성을 위해

import os
import ultralytics # YOLO 라이브러리 import
from ultralytics import YOLO
import cv2
from PIL import Image, ImageFont, ImageDraw
import numpy as np

# 2024.03.15 질문등록 question_create() 함수 추가
@login_required(login_url='common:login') # 2024.03.19 질문등록하려면 login 먼저하라고!
def question_create(request):
    """
    crowds 질문 등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            question.upload_image = request.FILES['upload_image']
            question.author = request.user # 추가한 속성 author 적용. 2024.03.19 
            question.create_date = timezone.now()
            question.save()

            # ======= YOLOv8 predict() 후에 답변을 자동 생성할까? ========== 
            yolo_predict(question)       
            
            # 답변 자동 생성 하기
            answer_create(request, question.id, question.upload_image,  )   

            return redirect('crowds:index')
    else :
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'crowds/question_form.html', context)

# 2024.03.19 질문수정함수 추가
@login_required(login_url='common:login') 
def question_modify(request, question_id):
    """
    crowds 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    # 로그인한 사용자(request.user)와 글쓴이(question.author)가 다르면 수정권한없음
    if request.user != question.author: 
        messages.error(request, '수정권한이 없습니다')
        return redirect('crowds:detail', question_id=question.id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False) # create_date가 지정될 때까지 임시저장
            question.author = request.user 
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()
            return redirect('crowds:detail', question_id=question.id)
    else :
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'crowds/question_form.html', context)

# 2024.03.19 질문삭제함수 추가
@login_required(login_url='common:login') 
def question_delete(request, question_id):
    """
    crowds 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    # 로그인한 사용자(request.user)와 글쓴이(question.author)가 다르면 삭제권한없음
    if request.user != question.author: 
        messages.error(request, '삭제권한이 없습니다')
        return redirect('crowds:detail', question_id=question.id)
    
    question.delete()
    return redirect('crowds:index')


# ============== YOLOv8 predict 관련 함수 start ==========================

# class별 건수 및 전체 건수 계산 함수
def count_objects(results, target_classes):

    total_counts = 0
    object_counts = {x: 0 for x in target_classes} # 0 으로 초기화

    for result in results: # predict() 결과가 저장된 results 변수 반복문
         for c in result.boxes.cls: # 예측결과에서 각 객체의 클래스ID
            c = int(c) # float타입 -> 정수형으로 변환
            '''
            target_classes : predict()에 넘겨준 관심 classes=[] 저장 리스트
            object_counts : 각 클래스별 객체 개수를 저장하는 딕셔너리
            '''
            if c in target_classes:
                object_counts[c] += 1
            elif c not in target_classes:
                object_counts[c] = 0

    for i in object_counts:
        if object_counts[i] >= 1 :
            total_counts += object_counts[i]

    return object_counts[0],total_counts # person, 전체 건수

# 이미지에 counter 넣기 함수
def plot_counter1(img, text1): # text 1 줄만 넣기
    font= cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    color = (0,255,0)
    thickness = 2

    h, w, c = img.shape # 이미지 크기(모양)를 읽어오자

    # 문자 넣을 x,y 위치 정하기
    org1_x = org2_x = w - 330
    org1_y = h - 30
    org1 =  (org1_x, org1_y)

    # img 변수가 NumPy 배열인지 확인
    if not isinstance(img, np.ndarray):
        # img_nparray = np.array(img)
        # img_nparray = np.asarray(img)
        raise TypeError("img 변수가 NumPy 배열이 아닙니다.")

    cv2.putText(img,text1,org1,font,fontScale,color,thickness,cv2.LINE_AA)

    # 이미지 출력해보자
    cv2.imshow('Image', img) # colab 이외 환경 (vscode, jupyter notebook 등)

# 추론/예측 함수

def yolo_predict(question):
    image_dir = './media/'
    # image_dir = "C:/projects/crowds/media/"
    out_dir = os.path.join(image_dir, "predict_images")
    source_image = os.path.join(image_dir, str(question.upload_image.name))
    predict_file = 'pred_' + os.path.split(source_image)[1]
    out_file = os.path.join(out_dir, predict_file) 
    
    choice = False
    
    if choice : # YOLOv8 original 모델 그대로 사용
        yolo_model = YOLO('yolov8n.pt') 
        
    else : # 전이학습 : YOLOv8 pretrained 모델 지정
        # pretrained_model = 'C:/projects/crowds/YOLOv8/best.pt'
        pretrained_model = './YOLOv8/best.pt'
        yolo_model = YOLO(pretrained_model) # 전이학습용
    
    # predict 예측/추론하기
    results = yolo_model.predict(source=source_image, conf=0.30,
                                 name=out_dir, save=True, exist_ok=True,
                                 seed=0, show_conf=False)
    
    # object detection 결과 : person, 전체 건수 계산
    person_count,total_counts = count_objects(results, yolo_model.names)
    
    # 이미지에 person 건수 쓰기
    cv2_image = cv2.imread(out_file)
    out_text1 = f'      [{person_count}] persons' # 이미지에 출력
    plot_counter1(cv2_image, out_text1)
    cv2.imwrite(out_file, cv2_image)
    
# ============== YOLOv8 predict 관련 함수 end ==========================