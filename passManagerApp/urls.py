from django.urls import path
from .views import home, notes, signup, login, confirmation, addpassword, addnote, addcard, cards, passwords, tools, updatenote, updatepassword, updatecard
urlpatterns = [
    path("", home, name="home"),
    path("notes", notes, name="notes"),
    path("passwords", passwords, name="passwords"),
    path("addnote", addnote, name="addnote"),
    path("updatenote/<note_id>", updatenote, name="updatenote"),
    path("updatepassword/<password_id>", updatepassword, name="updatepassword"),
    path("updatecard/<card_id>", updatecard, name="updatecard"),
    path("signup", signup, name="signup"),
    path("login", login, name="login"),
    path("confirmation", confirmation, name="confirmation"),
    path("addpassword", addpassword, name="addpassword"),
    path("addcard", addcard, name="addcard"),
    path("cards", cards, name="cards"),
    path("tools", tools, name="tools"),
]