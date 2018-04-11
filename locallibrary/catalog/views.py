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
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {'number_of_books': number_of_books, 'number_of_instances': number_of_instances,
               'num_instances_available': num_instances_available, 'num_authors': num_authors,
               'number_of_genre': number_of_genre, 'number_of_the_in_book_name': number_of_the_in_book_name,
               'num_visits': num_visits}
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'lists/book_list.html'
    paginate_by = 20

    # this is an approach for send extra data to template.
    # def get_context_data(self, **kwargs):
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     context['sample_value'] = "it's a sample value for test!"
    #     return context


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'lists/author_list.html'
    paginate_by = 20


class BookDetailView(generic.DeleteView):
    model = Book
    template_name = 'details/book_detail.html'


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'details/author_detail.html'
