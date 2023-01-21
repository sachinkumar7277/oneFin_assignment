from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from movie_collection.models import User, Movies, Collection


# Register your models here.
class UserAdmin(ModelAdmin):
    list_display = ['id', 'username', 'date_of_join']


admin.site.register(User, UserAdmin)


class MoviesAdmin(ModelAdmin):
    list_display = ['uuid', 'title', 'collection', 'created', 'updated']


admin.site.register(Movies, MoviesAdmin)


class CollectionAdmin(ModelAdmin):
    list_display = ['uuid', 'title','user', 'created', 'updated']


admin.site.register(Collection,CollectionAdmin)
