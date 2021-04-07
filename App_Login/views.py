from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required



def sign_up(request):
    form = UserCreationForm()
    registered = False
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save() 
            registered = True

    context = {
        'form': form,
        'registered':registered
    }        

    return render(request,'App_Login/signup.htm',context)        


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
    context = {
        'form':form
    }            

    return render(request,'App_Login/login.htm',context) 

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:sign_in'))              

