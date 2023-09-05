
from app1 import views
from django.urls import re_path as url

# template url tagging 
app_name = 'app1'

urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
]