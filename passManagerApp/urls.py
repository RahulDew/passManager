from django.urls import path
from .views import home, notes, signup, login, confirmation, addpassword, addnote, addcard, cards, passwords, tools
urlpatterns = [
    path("", home, name="home"),
    path("notes", notes, name="notes"),
    path("passwords", passwords, name="passwords"),
    path("addnote", addnote, name="addnote"),
    path("signup", signup, name="signup"),
    path("login", login, name="login"),
    path("confirmation", confirmation, name="confirmation"),
    path("addpassword", addpassword, name="addpassword"),
    path("addcard", addcard, name="addcard"),
    path("cards", cards, name="cards"),
    path("tools", tools, name="tools"),
]