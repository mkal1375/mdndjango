from django.contrib import admin
from .models import Genre, Book, BookInstance, Author, Language


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('genre',)

@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_filter = ('status', 'due_back')



admin.site.register(Genre)
admin.site.register(Language)
