from django.contrib import admin
from .models import Password
from .models import Note

# Register your models here.
admin.site.register(Password)
admin.site.register(Note)