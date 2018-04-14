from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/', RedirectView.as_view(pattern_name='books', permanent=False)),
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorListView.as_view(), name="authors"),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name="mybooks"),
    path('allborrowed/', views.AllLoanedBooksListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/create', views.BookCreateView.as_view(), name='create-book'),
    path('book/<int:pk>/delete', views.BookDeleteView.as_view(), name='delete-book'),
    path('book/<int:pk>/update', views.BookUpdateView.as_view(), name='update-book'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('book/create_instance', views.BookInstanceCreateView.as_view(), name='create-instance'),
    path('book/<uuid:pk>/update', views.BookInstanceUpdateView.as_view(), name='update-instance'),
    path('book/<uuid:pk>/delete', views.BookInstanceDeleteView.as_view(), name='delete-instance'),
    path('author/create', views.AuthorCreateView.as_view(), name='create-author'),
    path('author/<int:pk>/update', views.AuthorUpdateView.as_view(), name='update-author'),
    path('author/<int:pk>/delete', views.AuthorDeleteView.as_view(), name='delete-author'),
]
