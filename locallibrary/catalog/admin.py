from django.contrib import admin
from .models import Genre, Book, BookInstance, Author, Language
# Register your models here.

admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Author)
admin.site.register(Language)
