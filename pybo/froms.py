'''
파일명 : froms.py
설 명 :
생성일 : 2023-02-01
생성자 : AhnSeonghyun
since 2023.01.09 Copyright (C) by KandJang All right reserved.
'''
from django import forms
from pybo.models import Question

class QusetionForm(forms.ModelForm):
    class Meta:
        model = Question # 사용할 question model

        fields = ['subject', 'content'] # QusetionFormt에서 사용할 question model의 속성
        widgets = {
            #class = "form-control"
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows':10}),
        }
        labels ={ # subject -> 제목 으로 변경
            'subject':'제목',
            'content':'내용',
        }