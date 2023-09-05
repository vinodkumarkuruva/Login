from django.shortcuts import render
from app1.forms import UserForm,UserProfileInfoForm
from django.contrib.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def index(request):
    return render(request,'app1/index.html')



@login_required
def special(request):
    return HttpResponse("you are logined so,nice")



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data = request.POST) # user_form  and profile_form is injected from register.html file in app1
        
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save() # here we are saving the information in database by using the save

            user.set_password(user.pw) # here we are hashing the passwords
            
            user.save()

            profile= profile_form.save(commit=False) #here we made it false to avoid collision error 

            profile.user = user #(here user = user_form above) # here we are making onetoone relationhip

            if 'profile_pic' in request.FILES:

                profile.profilepic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:

            print(user_form.errors,profile_form.errors)

    else:

        user_form=UserForm()

        profile_form = UserProfileInfoForm()

    return render(request,'app1/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})



def user_login(request):

    if request.method=='POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:

            if user.is_active:

                login(request,user)

                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpResponse('account not active')
        
        else:

            print('someone tried to login and failed!')
            print('username:{} and password :{}'.format(username,password))
            return HttpResponse('invalid login details')
    else:

        return render(request,'app1/login.html',{})
