from django.contrib import admin



# Register your models here.
from users.models import CustomUser

admin.site.register(CustomUser)