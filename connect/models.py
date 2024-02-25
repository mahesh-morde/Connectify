from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    cat_choice = [
        (1, "Friends"),
        (2, "Family"),
        (3, "Office")
    ]

    name = models.CharField(max_length=255, verbose_name="Name")
    phone_number = models.CharField(max_length=20, verbose_name="Phon Number")
    email = models.EmailField()
    addtoFva = models.BooleanField(default=False)
    category = models.IntegerField(choices=cat_choice, blank=True)
    location = models.CharField(max_length=255)
    uname = models.CharField(max_length=255)


    def __str__(self):
        return self.name
    

