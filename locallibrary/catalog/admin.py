from django.contrib import admin
from .models import Genre, Book, BookInstance, Author, Language


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('genre',)
    fields = [('title', 'author'), 'summery', ('isbn', 'language'), 'genre']
    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_display = ('book', 'imprint', 'status', 'borrower')
    list_filter = ('status', 'due_back')
    fieldsets = (
        ('Info', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': [('status', 'due_back', 'borrower')]
        }),
    )



admin.site.register(Genre)
admin.site.register(Language)
