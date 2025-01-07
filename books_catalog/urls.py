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

    path('profile/history', views.issue_history, name='issue-history'),

    path('librarian/borrowed', views.AllLoanedListView.as_view(), name='all-borrowed-books'),
    path('librarian/update-settings', views.update_library_settings, name='update-library-settings'),
    path('book/<int:pk>/edit', views.update_book, name='update-book'),
    path('books/add', views.add_book, name='add-book'),

    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('book/<uuid:pk>/borrow', views.borrow_book, name='borrow-book'),
    path('book/<uuid:pk>/return/', views.return_book, name='return-book'),

    path('feedback/submit', views.submit_portal_feedback, name='submit-portal-feedback'),
    path('feedback/view', views.view_portal_feedback, name='view-portal-feedback'),

    path('search/', views.CatalogSearchView.as_view(), name='search'),
]