from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from movie_collection.models import User,Movies,Collection

# Register your models here.
admin.site.register(User)
admin.site.register(Movies)
admin.site.register(Collection)