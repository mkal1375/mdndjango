from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('/authors/', views.authors),
    path('/book/<int:id>', views.book),
    path('/author/<int:id>', views.author),
]