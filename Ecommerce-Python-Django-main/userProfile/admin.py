from django.contrib import admin
from .models import Account,Address,Profile

admin.site.register(Account)  
admin.site.register(Address)
admin.site.register(Profile)
# Register your models here.
