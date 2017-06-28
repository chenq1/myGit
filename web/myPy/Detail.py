#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from datetime import timedelta,datetime
from web.models import Thwdayrpt,Tztedayrpt,Tfhdayrpt

# 本类中有两个主要方法，checkDate方法是获取传递的数据，并通过计算返回查询的日期的相关数据，包括平台名称，查询日期，查询天数
# 第二个方法就是checkOut,具体查询数据库中相关数据，分成日报查询和周报查询，以字典形式返回查询到的数据，

class Detail:

    def __init__(self,form):
        self.form = form
    @staticmethod
    def setAddDay(date):
        setAddDay = date + timedelta(days=1)
        return setAddDay

    def checkDate(self):
        # 获取日期数据
        if 'dRptdate_year' in self.form.data.keys():
            platformname = self.form.data['platformname']
            dRptdate_year = self.form.data['dRptdate_year']
            dRptdate_month = self.form.data['dRptdate_month']
            dRptdate_day = self.form.data['dRptdate_day']
            date = dRptdate_year+'-'+dRptdate_month+'-'+dRptdate_day
            return {'platformname':platformname, 'date':date, 'day':1}    # 返回查询日期（字符串形式）

        if 'wRptstartdate_year' in self.form.data.keys():
            platformname = self.form.data['platformname']
            wRptstartdate_year = self.form.data['wRptstartdate_year']
            wRptstartdate_month = self.form.data['wRptstartdate_month']
            wRptstartdate_day = self.form.data['wRptstartdate_day']
            wRptenddate_year = self.form.data['wRptenddate_year']
            wRptenddate_month = self.form.data['wRptenddate_month']
            wRptenddate_day = self.form.data['wRptenddate_day']
            wRptstartdate = wRptstartdate_year + '-' + wRptstartdate_month + '-' + wRptstartdate_day
            wRptenddate = wRptenddate_year + '-' + wRptenddate_month + '-' + wRptenddate_day
            tmp_startdate = datetime.strptime(wRptstartdate, '%Y-%m-%d')
            tmp_enddate = datetime.strptime(wRptenddate, '%Y-%m-%d')
            day = (tmp_enddate - tmp_startdate).days + 1
            return {'platformname':platformname,'wRptstartdate':wRptstartdate,'wRptenddate':wRptenddate,'day':day}

    def checkOut(self):
        list1 = []      #存放获取的数据

        # 获取平台名称，如果有‘dRptdate_year’说明是日报查询
        platformname = self.form.data['platformname']
        if 'dRptdate_year' in self.form.data.keys():
            checkDate = self.checkDate()                            # 调用本类的另一个方法
            tmp_dayDate = datetime.strptime(checkDate['date'], "%Y-%m-%d")  # 把获得的日期数据转成date类型，再天数加1来查询
            daydate = self.setAddDay(tmp_dayDate)                   # 加一天
            day = daydate.strftime('%Y-%m-%d')                      # date类型转成字符串形式

            if platformname == 'HW':                            # 三个平台分别操作不同的类（获得数据库数据）
                return Thwdayrpt.objects.filter(updatetime__contains=day). \
                        values_list('nodename','avgwidth',
                            'sjjdll', 'peakjdll', 'jdllper',
                            'sjepgbf', 'peakepgbf', 'epgbfper',
                            'sjhmsbf', 'peakhmsbf', 'hmsbfper',
                            'sjdbkj', 'peakdbkj', 'dbkjper')
                return p

            elif platformname == 'zte':
                return Tztedayrpt.objects.filter(updatetime__contains=day).\
                        values_list('nodename','avgwidth',
                         'sjjdll','peakjdll','jdllper',
                         'sjepgbf','peakepgbf','epgbfper',
                         'sjhmsbf','peakhmsbf','hmsbfper',
                         'sjdbkj','peakdbkj','dbkjper')

            elif platformname == 'FH':
                return Tfhdayrpt.objects.filter(updatetime__contains=day).\
                        values_list('nodecname','quju','avgwidth',
                         'sjjdll','peakjdll','jdllper',
                         'sjjdbf','peakjdbf','jdbfper',
                         'sjdbkj','peakdbkj','dbkjper',
                         'mangguoll','mangguoper','number_4kll','number_4kper',
                         'youkull','youkuper','stbdown','stbdownper','bestvll','bestvoper',
                         'cesull','cesuper','boboll','boboper',
                         'tianyill','tianyiper','jiaoyull','jiaoyuper',
                         'huasull','huasuper','jiayoull','jiayouper','jylivell','jyliveper')

        # 如果有‘wRptstartdate_year’说明是月报查询，目前暂时将烽火这部分注释，之后会上线
        if 'wRptstartdate_year' in self.form.data.keys():
            checkDate = self.checkDate()                            # 调用本类的另一个方法
            tmp_startdate = datetime.strptime(checkDate['wRptstartdate'], "%Y-%m-%d")
            tmp_enddate = datetime.strptime(checkDate['wRptenddate'], "%Y-%m-%d")

            # 因为当天的数据一定是第二天才能获得统计结果，所以createtime是实际查询日期的第二天
            # 这里都是date类型的变量
            start = self.setAddDay(tmp_startdate)
            end = self.setAddDay(tmp_enddate)
            tmp_date = tmp_startdate

            #这里都是字符串类型的变量
            startday = start.strftime('%Y-%m-%d')   # createtime对应的开始时间（是查询开始时间的第二天）
            endday = end.strftime('%Y-%m-%d')       # createtime对应的结束时间（是查询结束时间的第二天）
            date = tmp_date.strftime('%Y-%m-%d')   # 显示查询数据的时间，存到list1中用于在页面显示正确数据时间

            while (startday <= endday):
                sumhms = 0
                sumepg = 0
                sumll = 0
                mangguoll = 0
                number_4kll = 0
                youkull = 0
                stbdown = 0
                bestvll = 0
                cesull = 0
                boboll = 0
                tianyill = 0
                jiaoyull = 0
                huasull = 0
                jiayoull = 0
                jylivell = 0

                if platformname == 'HW':
                    p = Thwdayrpt.objects.filter(updatetime__icontains=startday).values_list('peakhmsbf','peakepgbf','peakjdll')
                    for peakhmsbf,peakepgbf,peakjdll in p.iterator():
                        sumhms = sumhms + peakhmsbf
                        sumepg = sumepg + peakepgbf
                        sumll = sumll + peakjdll
                    tup = (str(date)[5:], int(sumhms), int(sumepg), int(sumll))

                if platformname == 'zte':
                    p = Tztedayrpt.objects.filter(updatetime__icontains=startday).values_list('peakhmsbf','peakepgbf','peakjdll')
                    for peakhmsbf,peakepgbf,peakjdll in p.iterator():
                        sumhms = sumhms + peakhmsbf
                        sumepg = sumepg + peakepgbf
                        sumll = sumll + peakjdll
                    tup = (str(date)[5:],int(sumhms),int(sumepg),int(sumll))

                if platformname == 'FH':
                    # 表数据还没，所以就暂时设置数据
                    sumyonghu = 8000
                    sumhms = 1000
                    sumepg = 1000
                    sumll = 70000
                    # 获取烽火各部分流量数据：芒果，4k，优酷，机顶盒，百事通，测速，播播，天翼，教育中心，华数，嘉攸，嘉攸直播
                    p = Tfhdayrpt.objects.filter(updatetime__icontains=startday).\
                        values_list('mangguoll','number_4kll','youkull','stbdown','bestvll',
                         'cesull','boboll','tianyill','jiaoyull','huasull','jiayoull','jylivell')
                    for mangguo,number_4k,youku,stb,bestv,cesu,bobo,tianyi,jiayu,huasu,jiayou,jylive in p.iterator():
                        mangguoll = mangguoll + mangguo
                        number_4kll = number_4kll + number_4k
                        youkull = youkull + youku
                        stbdown = stbdown + stb
                        bestvll = bestvll + bestv
                        cesull = cesull + cesu
                        boboll = boboll + bobo
                        tianyill = tianyill + tianyi
                        jiaoyull = jiaoyull + jiayu
                        huasull = huasull + huasu
                        jiayoull = jiayoull + jiayou
                        jylivell = jylivell + jylive

                    tup = (str(date)[5:],int(sumhms),int(sumepg),int(sumll),
                           int(mangguoll),int(number_4kll),int(youkull),int(stbdown),int(bestvll),int(cesull),
                           int(boboll),int(tianyill),int(jiaoyull),int(huasull),int(jiayoull),int(jylivell))
                    # print(tup)

                list1.append(tup)
                start = self.setAddDay(start)
                tmp_date = self.setAddDay(tmp_date)
                startday = start.strftime('%Y-%m-%d')  # createtime对应的开始时间（是查询开始时间的第二天）
                date = tmp_date.strftime('%Y-%m-%d')   # 显示查询数据的时间，存到list1中用于在页面显示正确数据时间
            return {'data':list1}
