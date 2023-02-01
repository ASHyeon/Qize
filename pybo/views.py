from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils import timezone
from .models import Question
from .froms import QusetionForm, AnswerForm
import logging


# Create your views here.

def question_create(request):
    '''질문등록'''

    logging.info('request.method:{}'.format(request.method))
    if request.method == 'POST':
        logging.info('question_create post')
        # 저장
        form = QusetionForm(request.POST) # request.POST 데이터

        if form.is_valid(): # form(질문등록)이 유효하면
            question=form.save(commit=False) # subject, content만 저장(commit은 하지 않음)
            question.create_date = timezone.now()
            question.save() # 날짜 까지 생성해서 저장(commit)
            return redirect("pybo:index")
    else:
        form = QusetionForm()
    context = {'form': form}
    return render(request,'pybo/question_form.html',context)


def boot_menu(request):
    '''개발에 사용되는 임시 메뉴'''
    return render(request,'pybo/menu.html')

def boot_reg(request):
    '''bootstrap template'''
    return render(request,'pybo/reg.html')

# bootstrap list
def boot_list(request):
    '''bootstrap template'''
    return render(request,'pybo/list.html')

def answer_create(request, question_id):
    logging.info('answer_create question_id:{}'.format(question_id))
    question = get_object_or_404(Question,pk=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer=form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save() # 최종 저장
            return redirect("pybo:detail",question_id)
    else:
        return HttpResponseNotAllowed('Post만 가능 합니다.')

    # form validation
    context = {'question':question, 'form':form}
    return render(request,'pybo:question_detail.html',context)

def detail(request, question_id):
    '''question 상세'''
    logging.info('1.question_id:{}', format(question_id))
    # question=Question.objects.get(id=question_id)
    question = get_object_or_404(Question,pk=question_id)
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
