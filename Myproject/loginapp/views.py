from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from  loginapp.models import Myuser
from examapp.models import Questions



def home(request):
    return render(request,"app1/home.html")

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile

def singup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        password2 = request.POST["confirm_password"]
        photo = request.FILES['photo']
        
        # Check if passwords match
        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("/singup")
        
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("/singup")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("/singup")

        # Create the user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        
        # Create the profile for the user
        profile = Profile(user=user, photo=photo)
        profile.save()

        # Redirect to login page
        return redirect("/login")
    
    return render(request, "app1/singup.html")

@login_required(login_url="/login")
def dashboard(request):
    if request.method=="GET":
        return render(request,"app1/dashboard.html")
    if request.method=="POST":
        return render(request,"app1/dashboard.html")
        

def logout(request):
    auth.logout(request)
    return redirect("/")


from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Profile

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Check if user has a profile
            # try:
            #     profile = Profile.objects.get(user=user)
            # except Profile.DoesNotExist:
            #     profile = None
            if user.is_superuser==1:
                return render(request,'app1/dashboard.html')
            # If profile does not exist, redirect to profile setup page
            # if not profile or not profile.photo:
            #     return redirect("/profile_setup")
            
            # Continue with dashboard if user has profile photo
            # return redirect("/dashboard")
            queryset=Questions.objects.all().values('subject').distinct()
            sub=list(queryset)
            print(f"subject is :-{queryset}")
            for op in queryset:
                print({f"subject is {op['subject']}"})
                request.session["answer"]={}
                request.session['username']=username
                request.session["qno"]=0
                request.session['questionindex']=0
                request.session["score"]=0
                request.session["w_score"]=0
                request.session["percentage"]=0
                request.session["subject"]=''
                questionlist=Questions.objects.all()

                question=questionlist[0]
                return render(request,'app1/startexam.html',{'question':question,'username':request.session['username'],'listofsubject':list(queryset),"message":"Loggin successfully"})
            else:
                return render(request,'app1/login.html',{"message":"username and password not found"})
    else:
        return render(request,"app1/login.html",{"message":"Invalid Credential"})
    return render(request, 'app1/login.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile
@login_required
def profile_setup(request):
    if request.method == "POST":
        photo = request.FILES['photo']
        
        # Update or create profile for the user
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.photo = photo
        profile.save()

        return redirect("/dashboard")  # Redirect to dashboard after upload
    
    return render(request, "app1/profile_setup.html")
