from django.conf.urls import url
from .views import *

app_name = 'dbms'

urlpatterns = [
    url(r'^user-register$', user_register, name='user-register'),
    url(r'^user-login$', user_login, name='user-login'),
    url(r'^admin-register$', admin_register, name='admin-register'),
    url(r'^admin-login$', admin_login, name='admin-login'),
    url(r'^admin/websites', AdminWebsiteView.as_view(), name='admin-website'),
    url(r'^keywords', KeywordsView.as_view(), name='keywords'),
    url(r'^log', get_log, name='get-log'),
    url(r'^get-result', get_result, name='get-result'),
    url(r'^hello', hello, name='hello')
]
