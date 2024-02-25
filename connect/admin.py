from django.contrib import admin
from .models import Contact


# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ["id","name","phone_number","email","addtoFva","category","location","uname"]
    list_filter = ['category', 'addtoFva','location',"uname"]

admin.site.register(Contact, ContactAdmin)

