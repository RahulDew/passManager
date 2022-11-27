from django.contrib import admin
from django.urls import path
from .views import *


# Django admin header customization
admin.site.site_header = "Welcome to ABSTRACTOR"
admin.site.site_title = "Abstractor Backend Dashboard"
admin.site.index_title = "ABSTRACTOR Administration"

urlpatterns = [
    path("", home, name="home"),
    path("signup", signup, name="signup"),
    path("login", login, name="login"),
    path("confirmation", confirmation, name="confirmation"),
    path("passwords", passwords, name="passwords"),
    path("notes", notes, name="notes"),
    path("cards", cards, name="cards"),
    path("addpassword", addpassword, name="addpassword"),
    path("addnote", addnote, name="addnote"),
    path("addcard", addcard, name="addcard"),
    path("updatepassword/<password_id>", updatepassword, name="updatepassword"),
    path("updatenote/<note_id>", updatenote, name="updatenote"),
    path("updatecard/<card_id>", updatecard, name="updatecard"),
    path("tools", tools, name="tools"),
    path("passgenerator", passgenerator, name="passgenerator"),
    path("pwnedPassCheck", pwnedPassCheck, name="pwnedPassCheck"),
]
