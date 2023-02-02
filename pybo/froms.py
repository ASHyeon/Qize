'''
파일명 : froms.py
설 명 :
생성일 : 2023-02-01
생성자 : AhnSeonghyun
since 2023.01.09 Copyright (C) by KandJang All right reserved.
'''
from django import forms
from pybo.models import Question, Answer

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer # 사용할 Answer model

        fields = ['content'] # AnswerForm 에서 사용할 Answer model의 속성

        labels = {
            'content': '답변내용',
        }

class QusetionForm(forms.ModelForm):
    class Meta:
        model = Question # 사용할 question model

        fields = ['subject', 'content'] # QusetionFormt에서 사용할 question model의 속성

        labels ={ # subject -> 제목 으로 변경
            'subject':'제목',
            'content':'내용',
        }