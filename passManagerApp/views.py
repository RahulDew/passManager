from django.contrib.auth.models import User
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as Login , logout
import random
from django.core.mail import send_mail
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
from .models import Password, Note
from django.contrib.auth.decorators import login_required

# from .models import Notes

br = Browser()
br.set_handle_robots(False)
fernet = Fernet(settings.KEY.encode())
# fernet = Fernet(settings.KEY.encode())



# Create your views here.

# def notes(request):
#     if request.user.is_authenticated:
#         user = request.user
#         print(user)
#         form = Notes(request.POST)
#         print("1111111")
#         if form.is_valid():
#             # print(form.cleaned_data)
#             print("222222")
#             todo = form.save(commit=False)
#             todo.user = user
#             todo.save()
#             print(todo)

#             print("33333")
#     return render(request, 'addnote.html')


def signup(request):
    if request.method == 'POST':
        if "signup-form" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirmPassword = request.POST.get("confirmPassword")
            # if password aren't identical
            if password != confirmPassword:
                msg = "please make sure you're using same password!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            
            # if user exists
            elif User.objects.filter(username=username).exists():
                msg = f"{username} already exists!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)

            # if email exists
            elif User.objects.filter(email=email).exists():
                msg = f"{email} already exists!"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            
            # create new user
            else:
                User.objects.create_user(username, email, password)
                new_user = authenticate(request, username=username, password=confirmPassword)
                if new_user is not None:
                    Login(request, new_user)
                    msg = f"{username} Thanks for subscribing!"
                    messages.error(request, msg)
                    return render(request, 'home.html')

    return render(request, 'signup.html')
    




def login(request):
    if request.method == 'POST':
        if "login-form" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            new_login = authenticate(request, username=username, password=password)
            if new_login is None:
                msg = f"Login failed! Make sure you're using the right account"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                code = str(random.randint(100000, 999999))
                global global_code
                global_code = code
                send_mail(
                    "Django Password Manager: confirm email",
                    f"Your verification code is {code}.",
                    settings.EMAIL_HOST_USER,
                    [new_login.email],
                    fail_silently=False,
                )
                return render(request, "confirmation.html", {
                    "code": code,
                    "user": new_login,
                })
    return render(request, 'login.html')
    



def confirmation(request):
    if request.method == 'POST':
        if "confirm-form" in request.POST:
            input_code = request.POST.get("code")
            user = request.POST.get("user")
            if input_code != global_code:
                msg = f"Confirmation code is wrong!"
                messages.error(request, msg)
                return render(request, 'home.html')
            else:
                Login(request, User.objects.get(username=user))
                msg = f"{request.user} Welcome Again"
                messages.success(request, msg)
                return render(request, 'home.html')

    return render(request, 'confirmation.html')


def addpassword(request):
    if request.method == 'POST':
        if "add-password" in request.POST:
            url = request.POST.get("url")
            email = request.POST.get("email")
            password = request.POST.get("password")
            #encrypt data
            encrypted_email = fernet.encrypt(email.encode())
            encrypted_password = fernet.encrypt(password.encode())
            # getting title of the website
            br.open(url)
            title = br.title()
            #get the logo of URL
            icon = favicon.get(url)[0].url
            # save data in database
            print("\n\n\n")
            print(encrypted_email)
            print(encrypted_password)
            print(title)
            print(icon)
            new_password = Password.objects.create(
                user = request.user,
                name = title,
                logo = icon,
                email = encrypted_email.decode(),
                password = encrypted_password.decode(),
            )
            msg = f"{title} added successfully"
            messages.success(request, msg)
            return render(request, 'home.html')
    return render(request, 'addpassword.html')

def addnote(request):
    print("IF ME JAA NHI RAHA H !!!")
    if request.method == 'POST':
        if "add-notes" in request.POST:
        # url = request.POST.get("url")
            print("IF ME JAA NHI RAHA H !!!")
            topic = request.POST.get("title")
            desc = request.POST.get("desc")
            print("ho rha h ")

            new_note = Note.objects.create(user = request.user, topic = topic, desc = desc)
            msg = f"{topic} Note added successfully"
            messages.success(request, msg)
            return render(request, 'home.html')
            # new_note.save()
    
        print("\n\n\n")
        print(topic)
        print(desc)
    return render(request, 'addnote.html')

def notes(request):
    context = {}
    if request.user.is_authenticated:
        notes = Note.objects.all().filter(user=request.user)
        for note in notes:
            note.topic = note.topic
            note.desc = note.desc
        context = {
            "notes": notes,
        }

    return render(request, 'notes.html', context)


def home(request):

    if request.method == 'POST':
        if "logout" in request.POST:
            logout(request)
            msg = f"You're logged out"
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
        elif "delete" in request.POST:
            to_delete = request.POST.get("password-id")
            msg = f"{Password.objects.get(id = to_delete).name} deleted successfully"
            Password.objects.get(id = to_delete).delete()
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
        
    context = {}
    if request.user.is_authenticated:
        passwords = Password.objects.all().filter(user=request.user)
        for password in passwords:
            password.email = fernet.decrypt(password.email.encode()).decode()
            password.password = fernet.decrypt(password.password.encode()).decode()
        context = {
            "passwords":passwords,
        }

    return render(request, 'home.html', context)
