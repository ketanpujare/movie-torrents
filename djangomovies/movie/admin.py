from django.contrib import admin

from .models        import Movie, Actor, Director, Genre
# Register your models here.

class ActorAdmin(admin.ModelAdmin):
    model = Actor
    filter_horizontal = ('movies',)

class DirectorAdmin(admin.ModelAdmin):
    model = Director
    filter_horizontal = ('movies',)

class GenreAdmin(admin.ModelAdmin):
    model = Genre
    filter_horizontal = ('movies',)

admin.site.register(Movie)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Genre, GenreAdmin)
