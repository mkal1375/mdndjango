from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorListView.as_view(), name="authors"),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name="mybooks"),
    path('allborrowed/', views.AllLoanedBooksListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/add', views.add_book, name='add-book'),
    path('book/<int:pk>/delete', views.delete_book, name='delete-book'),
    path('book/<int:pk>/edit', views.edit_book, name='edit-book'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]
