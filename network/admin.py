from django.contrib import admin
from .models import Posts, UserDetails

# Register your models here.
admin.site.register(Posts)
admin.site.register(UserDetails)