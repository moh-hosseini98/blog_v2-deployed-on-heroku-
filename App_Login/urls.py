from django.urls import path
from . import views

app_name = 'App_Login'

urlpatterns = [
    path('signup/',views.sign_up,name='sign_up'),
    path('signin/',views.login_page,name='sign_in'),
    path('logout/',views.logout_user,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('change-profile/',views.user_change,name='user_change'),
    path('password/',views.pass_change,name='pass_change'),
]