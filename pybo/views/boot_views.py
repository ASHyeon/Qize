'''
파일명 : boot_views.py
설 명 :
생성일 : 2023-02-08
생성자 : AhnSeonghyun
since 2023.01.09 Copyright (C) by KandJang All right reserved.
'''

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

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