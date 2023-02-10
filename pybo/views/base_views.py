'''
파일명 : base_views.py
설 명 :
생성일 : 2023-02-08
생성자 : AhnSeonghyun
since 2023.01.09 Copyright (C) by KandJang All right reserved.
'''

import logging
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import Question


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
    kw = request.GET.get('kw','') # 검색어
    div = request.GET.get('div','') # 검색어
    size = request.GET.get('size','10') # 페이지 기본값 10

    logging.info('page:{}'.format(page))
    logging.info('kw:{}'.format(kw))
    logging.info('div:{}'.format(div))

    question_list = Question.objects.order_by('-create_date') # order_by('-필드') desc, asc order_by('필드')

    #subject__contains : 사용 __contains또는 __icontains(대소 문자 구분) :
    if '10' == div:
        question_list = question_list.filter(subject__contains=kw)
    elif '20' == div:
        question_list = question_list.filter(content__contains=kw)
    elif '30' == div:
        # 포린키 관계 : author'__'username
        # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
        question_list = question_list.filter(author__username__contains=kw)


    # paging
    paginator=Paginator(question_list, size)
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
    context = {'question_list': page_obj, 'kw':kw, 'page':page, 'div':div, 'size':size }
    logging.info('question_list:{}'.format(page_obj))

    return render(request, 'pybo/question_list.html', context)
