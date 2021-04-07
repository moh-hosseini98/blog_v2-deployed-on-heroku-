from django.urls import path
from . import views

app_name = 'App_Login'

urlpatterns = [
    path('signup/',views.sign_up,name='sign_up'),
    path('signin/',views.login_page,name='sign_in'),
    path('logout/',views.logout_user,name='logout')
]