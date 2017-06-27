#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import codecs
import io
import mistune
import time
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.shortcuts import render

from web.myPy import Checkcode
from web.forms import LoginForm, DayRptForm,WeekRptForm, ChangepwdForm, UsrInPoolForm
from web.myPy.Detail import Detail
from web.myPy.Download import Download


def CheckCode(request):
    mstream = io.BytesIO()
    validate_code = Checkcode.create_validate_code()
    img = validate_code[0]
    img.save(mstream, "GIF")
    # 将验证码保存到session
    request.session["CheckCode"] = validate_code[1]
    return HttpResponse(mstream.getvalue())

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            check_code = request.POST.get('checkcode', '')
            session_code = request.session["CheckCode"]
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                if check_code.lower() != session_code.lower():
                    return render(request, 'login.html', {'form': form, 'check_code_is_wrong': True})
                else:
                    auth.login(request, user)
                    return HttpResponseRedirect("/accounts/index/")
            else:
                return render(request,'login.html',{'form': form, 'password_is_wrong': True})
        else:
            return render(request,'login.html', {'form': form})


@login_required
def index(request):
    request.user.username
    return render(request,'index.html',{request:'request'})


@login_required
def changepwd(request):
    if request.method == 'GET':
        form = ChangepwdForm()
        request.user.username
        return render(request, 'changepwd.html', {'form': form, request: 'request',})
    else:
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            newpassword1 = request.POST.get('newpassword1', '')
            newpassword2 = request.POST.get('newpassword2', '')
            user = auth.authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                print(newpassword1)
                if newpassword1 != newpassword2:
                    return render(request, 'changepwd.html', {'form': form, 'password_is_different': True})
                else:
                    user.set_password(newpassword1)
                    user.save()
                    return render(request, 'index.html', {'changepwd_success':True})
            else:
                return render(request, 'changepwd.html', {'form': form, 'oldpassword_is_wrong': True})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")


@login_required
def dRpt(request):
    if request.method == 'GET':
        request.user.username
        form = DayRptForm()
        return render(request, 'dRpt.html', {'form': form, request: 'request'})
    else:
        form = DayRptForm(request.POST)
        if form.is_valid():
            platformname = request.POST.get('platformname', '')
            if platformname is not None:
                info = Detail(form).checkDate       #获取开始查询的日期,天数
                form = Detail(form).checkOut        #获取查询到的数据
                if platformname != 'FH':
                    return render(request, 'detaildRpt1.html', {'form': form, 'info': info})
                else:
                    return render(request, 'detaildRpt2.html', {'form': form, 'info': info})
            else:
                return HttpResponse('输入有问题')
        else:
            return render(request,'dRpt.html',{'form':form})


@login_required
def wRpt(request):
    if request.method == 'GET':
        request.user.username
        form = WeekRptForm()
        return render(request, 'wRpt.html', {'form': form, request: 'request'})
    else:
        form = WeekRptForm(request.POST)
        if form.is_valid():
            platformname = request.POST.get('platformname', '')
            wRptstartdate_year = int(request.POST.get('wRptstartdate_year',''))
            wRptstartdate_month = int(request.POST.get('wRptstartdate_month',''))
            wRptstartdate_day = int(request.POST.get('wRptstartdate_day',''))
            wRptenddate_year = int(request.POST.get('wRptenddate_year',''))
            wRptenddate_month = int(request.POST.get('wRptenddate_month',''))
            wRptenddate_day = int(request.POST.get('wRptenddate_day',''))
            # 判断输入时间是否有问题
            if wRptenddate_year < wRptstartdate_year :
                return render(request, 'wRpt.html', {'form': form, 'date_is_wrong': True})
            elif wRptenddate_year == wRptstartdate_year :
                if wRptenddate_month < wRptstartdate_month:
                    return render(request, 'wRpt.html', {'form': form, 'date_is_wrong': True})
                elif wRptenddate_month == wRptstartdate_month:
                    if wRptenddate_day < wRptstartdate_day:
                        return render(request, 'wRpt.html', {'form': form, 'date_is_wrong': True})

            if platformname is not None:
                info = Detail(form).checkDate       #获取查询的日期,天数
                form = Detail(form).checkOut        #获取一个字典，里面两个list分别存有时间和数据
                if platformname != 'FH':
                    return render(request, 'detailwRpt1.html', {'form': form, 'info': info})
                else:
                    return render(request, 'detailwRpt2.html', {'form': form, 'info': info})
            else:
                return HttpResponse('输入有问题')
        else:
            return render(request,'wRpt.html', {'form': form})

@login_required
def download(request):
    day = request.GET['day']
    platformname = request.GET['platformname']
    if request.GET.get('wRptstartdate'):
        wRptstartdate = request.GET['wRptstartdate']
    else:
        wRptstartdate = 0
    if request.GET.get('wRptenddate'):
        wRptenddate = request.GET['wRptenddate']
    else:
        wRptenddate = 0
    if request.GET.get('date'):
        date = request.GET['date']
    else:
        date = 0
    data = {'date':date, 'wRptstartdate': wRptstartdate, 'wRptenddate': wRptenddate, 'day': day, 'platformname': platformname}

    # 生成文件，返回文件路径名称
    filename = Download(data).createFile()
    response = Download(data).downloadFile(filename)
    return response


'''
显示一个IP段内有多少用户和对应的区局
'''
@login_required
def usrs_in_ippool(request):
    time1 = time.time()
    ursinpool = UsrInPoolForm()
    if request.method == 'POST':
        form = UsrInPoolForm(request.POST)
        iplen = request.POST["iplen"]
        daylength = request.POST["daylength"]
        plat = request.POST["plat"]
        zero = request.POST.get("zero", "N")
        sip = request.POST.get("sip", "")

        args = (iplen, daylength, plat, sip,zero)
        rows = call_p3a_usrs_in_ippool(*args)
        rowslen = len(rows)
        time2 =time.time()
        timeminus = round(time2-time1,3)
        return render(request, 'usrs_in_ippool.html',{'rows': rows, 'timeminus': timeminus,'rowslen':rowslen, 'ursinpool': form})
    return render(request, 'usrs_in_ippool.html', {'ursinpool': ursinpool})

def call_p3a_usrs_in_ippool(*args):
    with connection.cursor() as cursor:
        cursor.callproc("pusrs_in_ippool_fin", args)
        rows = cursor.fetchall()
        cursor.close()
    return rows


@login_required
def version(request):
    input_file=codecs.open("/usr/local/www/IPTVweb/version.md",mode='r', encoding="utf-8")
    text=input_file.read()
    #renderer = mistune.Renderer(escape=False, hard_wrap=True)
    markdown=mistune.Markdown(escape=True, hard_warp=True)
    #markdown=mistune.Markdown(renderer=renderer)
    return render(request, 'version.html', {'version':markdown(text)})
    
