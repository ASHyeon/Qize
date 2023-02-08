import logging

import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .froms import QusetionForm, AnswerForm
from .models import Question, Answer

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

# Create your views here.
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)
    question.delete() # 삭제
    return redirect('pybo:index')

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

def crawling_cgv(request):
    '''CGV 무비차트'''
    '''CGV http://www.cgv.co.kr/movies/?lt=1&ft=0'''
    url = 'http://www.cgv.co.kr/movies/?lt=1&ft=0'
    response = requests.get(url)
    print(response.status_code)
    context = {}
    if 200 == response.status_code:
        html = response.text
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')
        # 제목
        title = soup.select('div.box-contents strong.title')
        # print(title)
        # 예매율
        rrr = soup.select('div.score strong.percent')
        # print(rrr)

        poster = soup.select('span.thumb-image img')

        title_list=[] #제목
        rrr_list =[] #예매율
        poster_list =[] #포스터
        for page in range(0, 7, 1):
            posterImg = poster[page]
            imgUrlPath = posterImg.get('src')   # <img src='' /> 에 접근
            title_list.append(title[page].getText())
            rrr_list.append(rrr[page].getText())
            poster_list.append(imgUrlPath)

            print(title[page].getText(), rrr[page].getText(), imgUrlPath)

        context = {'context':zip(title_list, rrr_list,poster_list)}

    else:
        print('접속오류')
    return render(request, 'pybo/crawling_cgv.html', context)

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


def boot_menu(request):
    '''개발에 사용되는 임시 메뉴'''
    return render(request, 'pybo/menu.html')


def boot_reg(request):
    '''bootstrap template'''
    return render(request, 'pybo/reg.html')


# bootstrap list
def boot_list(request):
    '''bootstrap template'''
    return render(request, 'pybo/list.html')

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


def detail(request, question_id):
    '''question 상세'''
    logging.info('1.question_id:{}', format(question_id))
    # question=Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    logging.info('2.question:{}', format(question))
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def index(request):
    '''question 목록'''
    # list order create_date desc
    # logging.info('index 레벨로 출력')

    # 입력인자
    page=request.GET.get('page','1') # 페이지
    logging.info('page:{}'.format(page))

    question_list = Question.objects.order_by('-create_date') # order_by('-필드') desc, asc order_by('필드')
    # paging
    paginator=Paginator(question_list, 10)
    page_obj=paginator.get_page(page)
    # paginator.count : 전체 게시물 개수
    # paginator.per_page : 페이지당 보여줄 게시물 개수
    # paginator.page_range : 페이지 범위
    # number : 현재 페이지 번호
    # previous_page_number : 이전 페이지 번호
    # next_page_number : 다음 페이지 번호
    # has_previous : 이전 페이지 유무
    # has_next : 다음 페이지 유무
    # start_index : 현재 페이지 시작 인덱스(1부터 시작)
    # end_index : 현재 페이지 끝 인덱스





    # question_list = Question.objects.filter(id=99)
    context = {'question_list': page_obj}
    logging.info('question_list:{}'.format(page_obj))

    return render(request, 'pybo/question_list.html', context)
