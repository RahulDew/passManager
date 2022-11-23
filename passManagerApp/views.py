from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as Login , logout
import random
from django.core.mail import send_mail
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
from .models import Password, Note, Card
from django.contrib.auth.decorators import login_required

# html email required stuff
# from django.core.mail import EmailMultiAlternatives # Main thingthis will help to send html email
# from django.template.loader import render_to_string # helps to render stuff dynamically
# from django.utils.html import strip_tags # so that we send content

br = Browser()
br.set_handle_robots(False)
fernet = Fernet(settings.KEY.encode())



# Create your views here.

# signup view

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
                return redirect('/')

            # if email exists
            elif User.objects.filter(email=email).exists():
                msg = f"{email} already exists!"
                messages.error(request, msg)
                return redirect('/')
            
            # create new user
            else:
                User.objects.create_user(username, email, password)
                new_user = authenticate(request, username=username, password=confirmPassword)
                if new_user is not None:
                    Login(request, new_user)
                    msg = f"{username} Thanks for subscribing!"
                    messages.error(request, msg)
                    return redirect('/')

                    # # sending the html email as welcome email
                    # html_content = render_to_string("email_template.html", {'title': 'Welcome Email'})
                    # text_content = strip_tags(html_content)

                    # welcome_email = EmailMultiAlternatives(
                    #     "Welcome_testing",
                    #     text_content,
                    #     settings.EMAIL_HOST_USER,
                    #     [email]
                    # )

                    # welcome_email.attatchaltranative(html_content, "text/html")
                    # welcome_email.send()

    return render(request, 'signup.html')
    



# login view

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
    


# confirmation view

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
                return redirect('/')

    return render(request, 'confirmation.html')



# addpassword view

def addpassword(request):
    if request.method == 'POST':
        if "add-password" in request.POST:
            name = request.POST.get("name")
            url = request.POST.get("url")
            email = request.POST.get("email")
            password = request.POST.get("password")
            #get the logo of URL
            try:
                icon = favicon.get(url)[0].url
            except:
                icon = "https://cdn-icons-png.flaticon.com/128/1006/1006771.png"
            #encrypt data
            encrypted_url = fernet.encrypt(url.encode())
            encrypted_email = fernet.encrypt(email.encode())
            encrypted_password = fernet.encrypt(password.encode())
            # getting title of the website
            # br.open(url)
            # title = br.title()
            # save data in database
            new_password = Password.objects.create(
                user = request.user,
                name = name,
                url = encrypted_url.decode(),
                logo = icon,
                email = encrypted_email.decode(),
                password = encrypted_password.decode(),
            )
            msg = f"{name} added successfully"
            messages.success(request, msg)
            return redirect('/passwords')
    return render(request, 'addpassword.html')

def updatepassword(request, password_id):
    password = Password.objects.get(id = password_id)
    password.url = fernet.decrypt(password.url.encode()).decode()
    password.email = fernet.decrypt(password.email.encode()).decode()
    password.password = fernet.decrypt(password.password.encode()).decode()

    if request.method == 'POST':
        if "update-password" in request.POST:
            password.name = request.POST.get("name")
            updated_url = request.POST.get("url")
            try:
                password.logo = favicon.get(password.url)[0].url
            except:
                password.logo = "https://cdn-icons-png.flaticon.com/128/1006/1006771.png"
            updated_email = request.POST.get("email")
            updated_password = request.POST.get("password")
            password.url = fernet.encrypt(updated_url.encode()).decode()
            password.email = fernet.encrypt(updated_email.encode()).decode()
            password.password = fernet.encrypt(updated_password.encode()).decode()
            password.save()
            
            msg = f"Your Password: {password.name} - Updated successfully"
            messages.success(request, msg)
            return redirect('/passwords')
    return render(request, 'updatepassword.html', { "password" : password })




# addnote view

def addnote(request):
    if request.method == 'POST':
        if "add-notes" in request.POST:
        # url = request.POST.get("url")
            topic = request.POST.get("topic")
            desc = request.POST.get("desc")
            #encrypt data
            encrypted_desc = fernet.encrypt(desc.encode()).decode()
            # save data in database
            new_note = Note.objects.create(user = request.user, topic = topic, desc = encrypted_desc)
            msg = f"Your Note: {topic} - added successfully"
            messages.success(request, msg)
            return redirect('/notes')
    
    return render(request, 'addnote.html')


def updatenote(request, note_id):
    note = Note.objects.get(id = note_id)
    note.topic = note.topic
    note.desc = fernet.decrypt(note.desc.encode()).decode()
    if request.method == 'POST':
        if "update-note" in request.POST:
            topic = request.POST.get("topic")
            desc = request.POST.get("desc")
            updated_desc = fernet.encrypt(desc.encode()).decode()
            note.topic = topic
            # note.desc = desc
            note.desc = updated_desc
            note.save()
            msg = f"Your Note: {topic} - Updated successfully"
            messages.success(request, msg)
            return redirect('/notes')
    return render(request, 'updatenote.html', { "note" : note })



#addcard view

def addcard(request):
    if request.method == 'POST':
        if "add-card" in request.POST:
            holder_name = request.POST.get("holder_name")
            bank_name = request.POST.get("bank_name")
            card_number = request.POST.get("card_number")
            key = request.POST.get("key")
            expiry_date = request.POST.get("expiry_date")

            #encrypt data
            encrypted_card_number = fernet.encrypt(card_number.encode())
            encrypted_key = fernet.encrypt(key.encode())
            encrypted_expiry_date = fernet.encrypt(expiry_date.encode())

            # saving data in database
            new_card = Card.objects.create(
                user = request.user,
                holder_name = holder_name,
                bank_name = bank_name,
                card_number = encrypted_card_number.decode(),
                key = encrypted_key.decode(),
                expiry_date = encrypted_expiry_date.decode(),
            )
            # printing message to home
            msg = f"{bank_name} Card added successfully"
            messages.success(request, msg)
            return redirect('/cards')

    return render(request, 'addcard.html')


def updatecard(request, card_id):
    card = Card.objects.get(id = card_id)
    card.card_number = fernet.decrypt(card.card_number.encode()).decode()
    card.key = fernet.decrypt(card.key.encode()).decode()
    card.expiry_date = fernet.decrypt(card.expiry_date.encode()).decode()

    if request.method == 'POST':
        if "update-card" in request.POST:
            # getting data from input
            holder_name = request.POST.get("holder_name")
            bank_name = request.POST.get("bank_name")
            updated_card_number = request.POST.get("card_number")
            updated_key = request.POST.get("key")
            updated_expiry_date = request.POST.get("expiry_date")
            #setting and encrypting data
            card.holder_name = holder_name
            card.bank_name = bank_name
            card.card_number = fernet.encrypt(updated_card_number.encode()).decode()
            card.key = fernet.encrypt(updated_key.encode()).decode()
            card.expiry_date = fernet.encrypt(updated_expiry_date.encode()).decode()
            card.save()

            msg = f"Your Card Detail: {card.bank_name} Card - Updated successfully"
            messages.success(request, msg)
            return redirect('/cards')

    return render(request, 'updatecard.html', { "card" : card })





# notes view

def notes(request):
    context = {}
    if request.user.is_authenticated:
        notes = Note.objects.all().filter(user=request.user)
        for note in notes:
            note.topic = note.topic
            # note.desc = note.desc
            note.desc = fernet.decrypt(note.desc.encode()).decode()

        context = {
            "notes": notes,
        }
    
    if request.method == 'POST':
        if "delete" in request.POST:
            to_delete = request.POST.get("note-id")
            msg = f"Your Note: {Note.objects.get(id = to_delete).topic} - Deleted successfully"
            Note.objects.get(id = to_delete).delete()
            messages.success(request, msg)
            return redirect('/notes')

    return render(request, 'notes.html', context)



# cards view

def cards(request):
    context = {}
    if request.user.is_authenticated:
        cards = Card.objects.all().filter(user=request.user)
        for card in cards:
            card.holder_name = card.holder_name
            card.bank_name = card.bank_name
            card.card_number = fernet.decrypt(card.card_number.encode()).decode()
            card.key = fernet.decrypt(card.key.encode()).decode()
            card.expiry_date = fernet.decrypt(card.expiry_date.encode()).decode()
            
        context = {
            "cards": cards,
        }
    
    if request.method == 'POST':
        if "delete" in request.POST:
            to_delete = request.POST.get("card-id")
            msg = f"{Card.objects.get(id = to_delete).bank_name} deleted successfully"
            Card.objects.get(id = to_delete).delete()
            messages.success(request, msg)
            return redirect('/cards')

    return render(request, 'cards.html', context)




def passwords(request):
    context = {}
    if request.user.is_authenticated:
        passwords = Password.objects.all().filter(user=request.user)
        for password in passwords:
            password.url = fernet.decrypt(password.url.encode()).decode()
            password.email = fernet.decrypt(password.email.encode()).decode()
            password.password = fernet.decrypt(password.password.encode()).decode()
        context = {
            "passwords":passwords,
        }
    
    if request.method == 'POST':
        if "delete" in request.POST:
            to_delete = request.POST.get("password-id")
            msg = f"{Password.objects.get(id = to_delete).name} deleted successfully"
            Password.objects.get(id = to_delete).delete()
            messages.success(request, msg)
            return redirect('/passwords')

    return render(request, 'passwords.html', context)


# home view

def home(request):

    if request.method == 'POST':
        if "logout" in request.POST:
            logout(request)
            msg = f"You're logged out"
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)

    return render(request, 'home.html')


def tools(request):

    return render(request, 'tools.html')

