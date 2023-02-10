'''
파일명 : question_views.py
설 명 :
생성일 : 2023-02-08
생성자 : AhnSeonghyun
since 2023.01.09 Copyright (C) by KandJang All right reserved.
'''

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..froms import QusetionForm
from ..models import Question

@login_required(login_url='common:login')
def question_vote(request, question_id):
    '''질문 : 좋아요'''
    logging.info('1. question_vote question_id:{} '.format(question_id))
    question = get_object_or_404(Question, pk=question_id)

    # 본인 글은 추천 하지 못하게
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        question.voter.add(request.user)

    return redirect('pybo:detail', question_id = question_id)

    pass


@login_required(login_url='common:login')
def question_modify(request, question_id):
    '''질문수정 : login 필수'''
    logging.info('1.question_modify')
    question = get_object_or_404(Question,pk=question_id) # question id로 Question 조회

    # 권한 체크
    if request.user != question.author:
        logging.info('2.question_modify post')
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id = question_id)

    if request.method == 'POST':
        form = QusetionForm(request.POST, instance=question)

        if form.is_valid():
            logging.info('3.form.is_valid()')
            question = form.save(commit=False) # 질문 내용,
            question.modify_date = timezone.now() # 수정일시 저장
            question.save()

            return redirect('pybo:detail', question_id = question_id)

    else:
        form = QusetionForm(instance=question)
    context = {'form':form}
    return render(request,'pybo/question_form.html',context)
    pass

@login_required(login_url='common:login') # 로그인이 되어있지 않으면 login 페이지로 이동
def question_create(request):
    '''질문등록'''

    logging.info('request.method:{}'.format(request.method))
    if request.method == 'POST':
        logging.info('question_create post')
        # 저장
        form = QusetionForm(request.POST)  # request.POST 데이터

        if form.is_valid():  # form(질문등록)이 유효하면
            question = form.save(commit=False)  # subject, content만 저장(commit은 하지 않음)
            question.create_date = timezone.now()
            question.author = request.user # author 속성에 로그인 계정 저장
            question.save()  # 날짜 까지 생성해서 저장(commit)
            return redirect("pybo:index")
    else:
        form = QusetionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)
    question.delete() # 삭제
    return redirect('pybo:index')