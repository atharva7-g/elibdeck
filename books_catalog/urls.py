from django.urls import path
from . import views

app_name = 'books_catalog'

urlpatterns = [
    path('', views.home, name='landing-page'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('profile/books', views.LoanedToUserListView.as_view(), name='profile-books'),
    path('librarian/borrowed', views.AllLoanedListView.as_view(), name='all-borrowed-books'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('search/', views.CatalogSearchView.as_view(), name='search'),
]