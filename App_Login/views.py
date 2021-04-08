from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import SignupForm,UserProfileChange,ProfilePic



def sign_up(request):
    form = SignupForm()
    registered = False
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
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

@login_required
def profile(request):
    return render(request,'App_Login/profile.htm')

@login_required
def user_change(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    if request.method == 'POST':
        form = UserProfileChange(request.POST,instance=current_user)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user)
            
    context = {
        'form':form
    }
    return render(request,'App_Login/change_profile.htm',context)        
      
@login_required
def pass_change(request):
    current_user = request.user
    change = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user,data=request.POST)
        if form.is_valid():
            form.save()
            change=True
    context = {
        'form':form,
        'change':change
    }        

    return render(request,'App_Login/pass_change.htm',context)        



@login_required
def add_pro_pic(request):
    form = ProfilePic()

    if request.method == 'POST':
        form = ProfilePic(request.POST,request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))

    context = {
        'form':form
    }        




    return render(request,'App_Login/pro_pic_add.htm',context)