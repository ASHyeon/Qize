'''
파일명 : pybo_filter.py
설 명 : 빼기 필터
생성일 : 2023-02-03
생성자 : AhnSeonghyun
since 2023.01.09 Copyright (C) by KandJang All right reserved.
'''

from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    ''' @register.filter : 템플릿에서 필터로 사용할수 있게 된다. (빼기 필터) '''
    return value - arg