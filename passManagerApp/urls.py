from django.urls import path
from .views import home, notes, signup, login, confirmation, addpassword, addnote
urlpatterns = [
    path("", home, name="home"),
    path("notes", notes, name="notes"),
    path("addnote", addnote, name="addnote"),
    path("signup", signup, name="signup"),
    path("login", login, name="login"),
    path("confirmation", confirmation, name="confirmation"),
    path("addpassword", addpassword, name="addpassword"),
]