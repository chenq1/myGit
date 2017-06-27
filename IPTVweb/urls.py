
from django.conf.urls import url
from django.contrib import admin
from web import views as web_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$',web_views.login,name='web_views_login'),
    url(r'^accounts/logout/$', web_views.logout, name='web_views_logout'),
    url(r'^checkcode/$',web_views.CheckCode,name='web_views_CheckCode'),

    url(r'^accounts/index/$', web_views.index, name='web_views_index'),
    url(r'^accounts/changepwd/$', web_views.changepwd, name='web_views_changepwd'),
    url(r'^accounts/usrs_in_ippool/$', web_views.usrs_in_ippool, name='web_views_ippool'),
    url(r'^accounts/dRpt/$', web_views.dRpt, name='web_views_dRpt'),
    url(r'^accounts/wRpt/$', web_views.wRpt, name='web_views_wRpt'),
    url(r'^accounts/download/$', web_views.download, name='web_views_download'),

    url(r'^accounts/version/$', web_views.version, name='web_views_version'),

]
