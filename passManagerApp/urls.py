from django.urls import path
from .views import *
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
    path("pwnedPassCheck", pwnedPassCheck, name="pwnedPassCheck"),
]
