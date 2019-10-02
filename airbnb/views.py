from django.shortcuts import render, redirect
from . import forms, models
from django.contrib import auth
from comp9900.settings import MEDIA_ROOT
import os

# Create your views here.


def index(request):
    return render(request, 'homePage.html')


def userRegister(request):
    message = ""
    if request.method == 'POST':
        registerForm = forms.UserRegisterForm(request.POST)
        if registerForm.is_valid():
            email = registerForm.cleaned_data['email']
            username = registerForm.cleaned_data['username']
            password = registerForm.cleaned_data['password']
            firstName = registerForm.cleaned_data['firstName']
            lastName = registerForm.cleaned_data['lastName']
            phone = registerForm.cleaned_data['phone']
            birthday = registerForm.cleaned_data['birthday']
            if not models.User.objects.filter(username=username).exists() \
                or not models.User.objects.filter(email=email):
                newGuest = models.User()
                newGuest.email = email
                newGuest.username = username
                newGuest.set_password(password)
                newGuest.first_name = firstName
                newGuest.last_name = lastName
                newGuest.phone = phone
                newGuest.birthday = birthday
                newGuest.save()
                message = "register successful!"
                return redirect('/index/')
            else:
                message = "username or email already exists"
        else:
            message = "invalid input"
    else:
        RegisterForm = forms.UserRegisterForm()

    return render(request, "userRegister.html", locals())


def userLogin(request):
    message = ""
    if request.method == 'POST':
        user = None
        loginForm = forms.UserForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
        if user and models.User.objects.filter(username=username).exists():
            auth.login(request, user)
            return redirect('/index/')
        else:
            message = "User doesn't exist or password is incorrect!"
            return render(request, "userLogin.html", locals())
    else:
        loginForm = forms.UserForm()
        return render(request, "userLogin.html", locals())


def updateUserInfo(request):
    if request.method == 'POST':
        form = forms.UserInfoUpdateForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            phone = form.cleaned_data['phone']
            birthday = form.cleaned_data['birthday']
            description = form.cleaned_data['description']

            user = models.User.objects.get(id=request.user.id)
            user.email = email
            user.first_name = firstName
            user.last_name = lastName
            user.phone = phone
            user.birthday = birthday
            user.description = description
            user.save()

            return redirect('/updateUserInfo/')

    dict = {}
    user = models.User.objects.get(id=request.user.id)
    if user.email:
        dict['email'] = user.email
    if user.first_name:
        dict['firstName'] = user.first_name
    if user.last_name:
        dict['lastName'] = user.last_name
    if user.phone:
        dict['phone'] = user.phone
    if user.birthday:
        dict['birthday'] = user.birthday
    if user.description:
        dict['description'] = user.description

    photo = "/pictures/e1b5f44d998ccbf08cf5571d45e93cbb.png"
    if user.portrait:
        photo = user.portrait

    InitialUserForm = forms.UserInfoUpdateForm(initial=dict)
    FileForm = forms.FileForm()
    return render(request, 'updateUserInfo.html', locals())


def portraitUpload(request):
    if request.method == 'POST':
        pic = request.FILES.get('file')
        user = models.User.objects.get(id=request.user.id)
        url = os.path.join(MEDIA_ROOT, pic.name)
        with open(url, 'w+b') as f:
            for data in pic.chunks():
                f.write(data)
        user.portrait = "pictures/" + pic.name
        user.save()
    return redirect('/updateUserInfo/')


def logout(request):
    auth.logout(request)
    return redirect('/index/')