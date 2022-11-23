from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    url = models.CharField(max_length=300, default='url')
    logo = models.CharField(max_length=300)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-id"]


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topic_content_type")
    topic = models.CharField(max_length=200)
    desc = models.CharField(max_length=4000)
    created_date = models.DateField(auto_now_add=True, auto_now=False)
    created_time = models.TimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ["-id"]
        

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="card")
    holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=400) # we don't using IntegerField and DateField because when we encrypting the data
    key = models.CharField(max_length=400)         # our data converted into collection of multile character, integer and symbol  
    expiry_date = models.CharField(max_length=400) # and then it throw an error that int() ant assign that value

    def __str__(self):
        return self.holder_name

    class Meta:
        ordering = ["-id"]

