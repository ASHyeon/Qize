from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils import timezone
from .models import Question
from .froms import QusetionForm, AnswerForm
from bs4 import BeautifulSoup
import requests
import logging



# Create your views here.

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

        context = {'title': title_list, 'rrr':rrr_list, 'poster':poster_list}

    else:
        print('접속오류')
    return render(request, 'pybo/crawling_cgv.html', context)

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
            answer.save()  # 최종 저장
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Post만 가능 합니다.')
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
    logging.info('index 레벨로 출력')
    question_list = Question.objects.order_by('-create_date')  # order_by('-필드') desc, asc order_by('필드')
    # question_list = Question.objects.filter(id=99)
    context = {'question_list': question_list}

    return render(request, 'pybo/question_list.html', context)
