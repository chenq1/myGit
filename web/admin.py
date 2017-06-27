#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from django.contrib import admin
from web.models import  Tztedayrpt


class TztedayrptAdmin(admin.ModelAdmin):
    list_display = ('nodename', 'avgwidth', 'sjjdll','peakjdll','jdllper','sjepgbf','peakepgbf','epgbfper')


admin.site.register(Tztedayrpt,TztedayrptAdmin)