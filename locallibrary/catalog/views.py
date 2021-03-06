import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Book, Author, BookInstance, Genre, User
from .forms import RenewBookForm, AddBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django import forms


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


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'book_renew_librarian.html', {'form': form, 'bookinstance': book_instance})


# Replaced by create generic view class.
# @permission_required('catalog.can_create')
# def add_book(request):
#     form = AddBookForm(request.POST)
#
#     if request.method == "POST":
#         if form.is_valid():
#             book = Book()
#             book.title = form.cleaned_data['title']
#             book.author = form.cleaned_data['author']
#             book.language = form.cleaned_data['language']
#             book.isbn = form.cleaned_data['isbn']
#             book.summary = form.cleaned_data['summary']
#             book.save()
#             book.genre.set(form.cleaned_data['genre'])
#             book.save()
#
#             return HttpResponseRedirect(reverse('books'))
#
#     return render(request, 'add_book.html', context={'form': form})

# Replaced by generic confirm page in BookDeleteView class.
# def are_you_sure_delete_book(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     return render(request, 'are_you_sure.html', context={'type': 'book', 'data': book})


# Replaced by delete generic view class.
# def delete_book(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     book.delete()
#     return HttpResponseRedirect(reverse('books'))


# Book Model:
class BookCreateView(CreateView):
    model = Book
    fields = '__all__'
    template_name = 'book/book_create.html'


class BookUpdateView(UpdateView):
    model = Book
    fields = '__all__'
    template_name = 'book/book_update.html'


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    template_name = 'book/book_confirm_delete.html'


# BookInstance Model:
class BookInstanceCreateView(CreateView):
    # TODO: add feature / add patch(book/<int:book_id>/create_instance and add link on books list.
    model = BookInstance
    fields = '__all__'
    template_name = 'bookinstance/bookinstance_create.html'


class BookInstanceUpdateView(UpdateView):
    model = BookInstance
    fields = '__all__'
    template_name = 'bookinstance/bookinstance_update.html'


class BookInstanceDeleteView(DeleteView):
    model = BookInstance
    template_name = 'bookinstance/bookinstance_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('book-detail', args=(self.object.book.id,))


# Author Model:

class AuthorCreateView(CreateView):
    model = Author
    fields = '__all__'
    template_name = 'author/author_create.html'
    # TODO: add date picker for date fields.


class AuthorUpdateView(UpdateView):
    model = Author
    fields = '__all__'
    template_name = 'author/author_update.html'
    # TODO: add date picker for date fields.


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'author/author_confirm_delete.html'
    success_url = reverse_lazy('authors')


def lending(request, instance_id, user_id, due_back=None):
    try:
        instance = get_object_or_404(BookInstance, pk=instance_id)
        member = get_object_or_404(User, pk=user_id)
        if instance.status == 'o':
            return JsonResponse({'status': False, 'borrower':instance.borrower.id, 'exception': 'This copy has been borrowed.'})
        elif instance.status != 'a':
            return JsonResponse({'status': False, 'instance-status': instance.status, 'exception': 'This copy id not available.'})
        instance.borrower = member
        instance.status = 'o'
        if due_back != None:
            due_back = datetime.datetime.strptime(due_back,'%Y-%d-%m').date()
            timedelta = (due_back - datetime.date.today())
            if  timedelta.days < 0:
                return JsonResponse({'status': False, 'exception': 'due back is in past'})
            elif timedelta.days > 21:
                return JsonResponse({'status': False, 'exception': 'over max! max lent days is 21 (3 week)'})
        else:
            instance.due_back = datetime.date.today() + datetime.timedelta(weeks=3)
        instance.save()
    except Exception as e:
        return JsonResponse({'status': False, 'exception': str(e)})
    return JsonResponse({'status': True, 'instance_id':instance_id, 'member_id':user_id})

def backing(request, instance_id):
    try:
        instance = get_object_or_404(BookInstance, pk=instance_id)
        if instance.status != 'o':
            return JsonResponse(
                {'status': False, 'exception': 'This copy has not been borrowed'})
        borrower_id = instance.borrower.id
        instance.borrower = None
        instance.status = 'a'
        instance.due_back = None
        instance.save()
    except Exception as e:
        return JsonResponse({'status':False, 'exception':str(e)})
    return JsonResponse({'status': True, 'borrower': borrower_id, 'instance-id': instance.id})