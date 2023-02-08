'''
파일명 : answer_views.py
설 명 :
생성일 : 2023-02-08
생성자 : AhnSeonghyun
since 2023.01.09 Copyright (C) by KandJang All right reserved.
'''

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..froms import AnswerForm
from ..models import Question, Answer


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request,'삭제 권한이 없습니다')
        return redirect('pybo:detail', question_id = answer.question.id)
    answer.delete()  # 삭제
    return redirect('pybo:detail', question_id = answer.question.id)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    # 1. answer id에 해당되는 데이터 조회
    # 2. 수정 권한 체크:
    # 3. POST : 수정 , GET : 수정 Form 전달

    # 1.
    answer = get_object_or_404(Answer, pk=answer_id )

    # 2.
    if request.user != answer.author:
        messages.error(request,'수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)

    # 3.
    if request.method == 'POST': # 화면에 데이터를받아서 수정하는것
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer=form.save(commit=False)
            answer.modify_date=timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:                        # 수정 form의 template
        form = AnswerForm(instance=answer)
    context={'answer':answer, 'form':form}
    return render(request,'pybo/answer_form.html',context)

@login_required(login_url='common:login') # 로그인이 되어있지 않으면 login 페이지로 이동
def answer_create(request, question_id):
    '''답변등록'''
    print('answer_create question_id:{}'.format(question_id))
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        print('1.request.method:{}'.format(request.method))
        if form.is_valid():
            print('2.form.is_valid():{}'.format(form.is_valid()))
            answer = form.save(commit=False)  # content만 저장(commit은 하지 않음)
            answer.create_date = timezone.now()
            answer.question = question
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.save()  # 최종 저장
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    # form validation
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)