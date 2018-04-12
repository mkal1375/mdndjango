from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class BookListView(LoginRequiredMixin, generic.ListView):
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


# list view for book instances ... you need just inherit this.
class BookInstanceListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    paginate_by = 20


class LoanedBooksByUserListView(BookInstanceListView):
    template_name = 'lists/loaned_book_list.html'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllLoanedBooksListView(PermissionRequiredMixin, BookInstanceListView):
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    template_name = 'lists/all_borrowed.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
