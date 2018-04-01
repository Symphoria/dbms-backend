from django.conf.urls import url
from .views import *

app_name = 'dbms'

urlpatterns = [
    url(r'^user-register', user_register, name='user-register'),
    url(r'^admin-register', admin_register, name='admin-register')
]
