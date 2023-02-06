from django.test import TestCase

# Create your tests here.
import unittest
import datetime
import logging
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pyperclip # 클립보드를 쉽게 황용할 수 있게 해주는 모듈
from selenium.webdriver.common.keys import Keys # Ctrl+c, Ctrl+v


class Crawling(unittest.TestCase):

    def setUp(self):
        # webdriver Firefox 객체 생성
        self.brower = webdriver.Firefox(executable_path='C:\BIG_AI0102\01_PYTHON\app\geckodriver')
        print('setup')

    def tearDown(self):
        print('tearDown')
        # self.brower.quit()  # 브라우저 종료

    @unittest.skip('테스트')
    def test_naverLogin(self):
        self.brower.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')

        naver_id = self.brower.find_element(By.ID, 'id')
        naver_id.send_keys('mies123456')

        naver_pw = self.brower.find_element(By.ID, 'pw')
        naver_pw.send_keys('tjdgus4578!m@')

        naver_loginBtn = self.brower.find_element(By.ID, 'log.login')
        naver_loginBtn.click()
        pass

    def test_clipboard_naver(self):
        ''' clipboard를 통한 naver login '''
        self.brower.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
        user_id = 'mies123456'
        user_pw = 'tjdgus4578!m@'

        # 아이디
        id_textinput = self.brower.find_element(By.ID,'id')
        id_textinput.click()

        # 클립보드로 copy
        pyperclip.copy(user_id)
        id_textinput.send_keys(Keys.CONTROL,'v') # 클립보드에서 id textinput으로 copy
        time.sleep(1)

        # 비밀번호
        pw_textinput = self.brower.find_element(By.ID,'pw')
        pw_textinput.click()
        pyperclip.copy(user_pw)
        pw_textinput.send_keys(Keys.CONTROL,'v')
        time.sleep(1)

        # 로그인 버튼
        btn_login = self.brower.find_element(By.ID, 'log.login')
        btn_login.click()

        pass

    @unittest.skip('테스트')
    def test_selenium(self):
        # FireFox 웹 드라이버 객체에게 Get을 통하여 네이버의 http요청을 하게 함.
        self.brower.get('http://127.0.0.1:8000/pybo/4/')
        print('self.brower.title:{}'.format(self.brower.title))
        self.assertIn('Pybo', self.brower.title)

        content_textarea=self.brower.find_element(By.ID,'content')
        content_textarea.send_keys('운동가기싫다.....')

        context_btn = self.brower.find_element(By.ID, 'context_btn')
        context_btn.click()



        pass

    @unittest.skip('테스트')
    def text_zip(self):
        ''' 여러개의 list를 묶어서 하나의 iterable객체로 다루수 있게 한다. '''
        intergers = [1, 2, 3]
        letters = ['a', 'b', 'c']
        floats = [4.0, 8.0, 10.0]
        zipped = zip(intergers, letters, floats)
        list_data = list(zipped)
        print(list_data)


    @unittest.skip('테스트')
    def test_naver_stock(self):
        '''주식 크롤링'''
        codes = {'삼성전자': '005930', '현대차': '005380'}
        for code in codes.keys():
            url = 'https://finance.naver.com/item/main.naver?code='
            # print(codes[code])
            url = url + str(codes[code])
            # print('url:{}'.format(url))
            response = requests.get(url)
            if 200 == response.status_code:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                # 제목
                price = soup.select_one('#chart_area div.rate_info div.today span.blind')
                # print('price:{}'.format(price.getText()))
                # today=price.select_one('.blind')
                print('today:{},{},{}'.format(code, codes[code], price.getText()))
            else:
                print('접속 오류 response.status_code:{}'.format(response.status_code))
        pass


    @unittest.skip('테스트')
    def call_slemdumk(self, url):
        response = requests.get(url)
        if 200 == response.status_code:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            # 평점
            score = soup.select('div.list_netizen_score em')
            # 감상평
            review = soup.select('table tbody tr td.title')

            for i in range(0, len(score)):
                review_text = review[i].getText().split('\n')

                if len(review_text) > 2:  # 평점만 넣고 감상평이 없는 경우 처리
                    tmp_text = review_text[5]
                else:
                    tmp_text = review_text[0]

                print('평점, 감상평:{},{}'.format(score[i].getText(), tmp_text))
        else:
            print('접속오류')


    def test_slemdumk(self):
        url = 'https://movie.naver.com/movie/point/af/list.naver?st=mcode&sword=223800&page='
        for i in range(1, 4, 1):
            self.call_slemdumk(url + str(i))


    @unittest.skip('테스트')
    def test_cgv(self):
        '''CGV http://www.cgv.co.kr/movies/?lt=1&ft=0'''
        url = 'http://www.cgv.co.kr/movies/?lt=1&ft=0'
        response = requests.get(url)
        print(response.status_code)
        if 200 == response.status_code:
            html = response.text
            # print(html)
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.select('div.box-contents strong.title')
            # print(title)

            rrr = soup.select('div.score strong.percent')
            # print(rrr)

            poster = soup.select('span.thumb-image img')

            for page in range(0, 7, 1):
                posterImg = poster[page]
                imgUrlPath = posterImg.get('src')
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
        print('=' * 35)
        print(newDate)
        print('=' * 35)

        # ------------------------------------------------
        naverWetherUrl = 'https://weather.naver.com/today/15200253'
        html = urlopen(naverWetherUrl)
        bsObject = BeautifulSoup(html, 'html.parser')
        tmpes = bsObject.find('strong', 'current')
        print('아산시 배방읍 날씨:{}'.format(tmpes.getText()))

        print('test_weather')
