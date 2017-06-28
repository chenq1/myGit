#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget, widgets

PLATFORM_CHOICES=(
    ('HW','华为'),('zte','中兴'),('FH','烽火')
)

YEAR_CHOICES = ('2017','2018','2019')

IPLEN_CHOICES = (
	('128C','128C'),('1B','1B'),('4B','4B')
)
DAY_CHOICES = (
	('1','1天内'),('31','31天内')
)
PLAT_CHOICES = (
	('HW','华为'),('zte','中兴')
)


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"用户名",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"用户名",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"密码",
            }
        ),
    )
    checkcode = forms.CharField(
        required=True,
        label=u"验证码",
        error_messages={'required': u'请输入验证码'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"验证码",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise ValidationError(u"用户名和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()


class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"原密码",
            }
        ),
    )
    newpassword1 = forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"新密码",
            }
        ),
    )
    newpassword2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"确认密码",
            }
        ),
    )
    def clean(self):
        if not self.is_valid():
            raise ValidationError(u"所有项都为必填项")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
            return cleaned_data


class DayRptForm(forms.Form):
    platformname = forms.ChoiceField(
        required=True,
        label = u"平台",
        error_messages={'required': u'请选择平台'},
        widget=forms.RadioSelect,
        choices=PLATFORM_CHOICES,
    )
    dRptdate = forms.DateField(
        required=True,
        label = u"查询日期",
        error_messages={'required': u'请选择日期'},
        widget=SelectDateWidget(
            years=YEAR_CHOICES,
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"必填")
        else:
            cleaned_data = super(DayRptForm, self).clean()
            return cleaned_data


class WeekRptForm(forms.Form):
    platformname = forms.ChoiceField(
        required=True,
        label = u"平台",
        error_messages={'required': u'请选择平台'},
        widget=forms.RadioSelect, choices=PLATFORM_CHOICES,
    )
    wRptstartdate = forms.DateField(
        required=True,
        label = u"开始查询日期",
        error_messages={'required': u'请选择日期'},
        widget=SelectDateWidget(years=YEAR_CHOICES),
    )
    wRptenddate = forms.DateField(
        required=True,
        label = u"截止查询日期",
        error_messages={'required': u'请选择日期'},
        widget=SelectDateWidget(years=YEAR_CHOICES,),
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"必填")
        else:
            cleaned_data = super(WeekRptForm, self).clean()
            return cleaned_data


class UsrInPoolForm(forms.Form):
    iplen = forms.CharField(
        widget = forms.Select(choices=IPLEN_CHOICES),
        initial=IPLEN_CHOICES[1][0],
        label='IP段：'
    )
    daylength = forms.CharField(
        widget = forms.Select(choices=DAY_CHOICES),
        initial=DAY_CHOICES[1][0],
        label = "查询天数："
    )
    plat = forms.CharField(
        widget=forms.Select(choices=PLAT_CHOICES),
        label = '查询平台：'
    )
    #zero = forms.CharField(widget=forms.CheckboxInput(), label='是否显示0用户IP段')
    zero = forms.BooleanField(
        widget = forms.CheckboxInput,
        required=False,
        label='是否显示0用户IP段？ '
    )
    sip = forms.GenericIPAddressField(
        protocol = 'IPv4',
        required = False,
        label='单个IP：'
    )


