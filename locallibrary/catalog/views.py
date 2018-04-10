from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre


def index(request):
    number_of_books = Book.objects.all().count()
    number_of_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.all().count()
    number_of_genre = Genre.objects.all().count()
    number_of_the_in_book_name = Book.objects.filter(title__icontains="the").count()
    context = {'number_of_books': number_of_books, 'number_of_instances': number_of_instances,
               'num_instances_available': num_instances_available, 'num_authors': num_authors,
               'number_of_genre': number_of_genre, 'number_of_the_in_book_name': number_of_the_in_book_name}
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'lists/book_list.html'
    queryset = Book.objects.filter(title__icontains=' a ')

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['sample_value'] = "it's a sample value for test!"
        return context

def authors():
    return None


def book():
    return None


def author():
    return None
