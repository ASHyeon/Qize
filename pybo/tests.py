from django.test import TestCase

# Create your tests here.
import unittest
import datetime
import logging
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen



class Crawling(unittest.TestCase):

    def setUp(self):
        print('setup')

    def tearDown(self):
        print('tearDown')

    def test_naver_stock(self):
        '''주식 크롤링'''
        url = 'https://finance.naver.com/item/main.naver?code=005380'
        response = requests.get(url)
        if 200 == response.status_code:
            html = response.text
            soup = BeautifulSoup(html,'html.parser')

            # 현대차 가격
            pre = soup.select('div.today em.no_up')


    def call_slemdumk(self,url):
        response=requests.get(url)
        if 200 == response.status_code:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            # 평점
            score = soup.select('div.list_netizen_score em')
            # 감상평
            review = soup.select('table tbody tr td.title')

            for i in range(0, len(score)):
                review_text = review[i].getText().split('\n')

                if len(review_text) > 2: # 평점만 넣고 감상평이 없는 경우 처리
                    tmp_text = review_text[5]
                else:
                    tmp_text = review_text[0]

                print('평점, 감상평:{},{}'.format(score[i].getText(), tmp_text))
        else:
            print('접속오류')


    def test_slemdumk(self):
        url = 'https://movie.naver.com/movie/point/af/list.naver?st=mcode&sword=223800&page='
        for i in range(1,4,1):
            self.call_slemdumk(url+str(i))



    @unittest.skip('테스트')
    def test_cgv(self):
        '''CGV http://www.cgv.co.kr/movies/?lt=1&ft=0'''
        url = 'http://www.cgv.co.kr/movies/?lt=1&ft=0'
        response=requests.get(url)
        print(response.status_code)
        if 200 == response.status_code:
            html=response.text
            # print(html)
            soup=BeautifulSoup(html,'html.parser')
            title=soup.select('div.box-contents strong.title')
            # print(title)

            rrr=soup.select('div.score strong.percent')
            # print(rrr)

            poster = soup.select('span.thumb-image img')


            for page in range(0,7,1):
                posterImg=poster[page]
                imgUrlPath=posterImg.get('src')
                print(title[page].getText(), rrr[page].getText(), imgUrlPath)


        else:
            print('접속오류')

    @unittest.skip('테스트연습')
    def test_weather(self):
        '''날씨'''
        # https://weather.naver.com/today/15200253
        now = datetime.datetime.now()
        # yyyymmdd hh:mm
        newDate = now.strftime('%Y-%m-%d %H:%M:%S')
        print('='*35)
        print(newDate)
        print('='*35)

        #------------------------------------------------
        naverWetherUrl = 'https://weather.naver.com/today/15200253'
        html = urlopen(naverWetherUrl)
        bsObject=BeautifulSoup(html,'html.parser')
        tmpes=bsObject.find('strong','current')
        print('아산시 배방읍 날씨:{}'.format(tmpes.getText()))

        print('test_weather')
