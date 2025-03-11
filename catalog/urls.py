from django.urls import path
from . import views

urlpatterns = [
    # catalog/ — The home (index) page.
    path("", views.index, name="index"),
    # catalog/books/ — A list of all books.
    path("books/", views.BookListView.as_view(), name="books"),
    # catalog/authors/ — A list of all authors.
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    # catalog/book/<id> — The detail view for a particular book, with a field primary key of <id> (the default). For example, the URL for the third book added to the list will be /catalog/book/3.
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book-detail"),
    # catalog/author/<id> — The detail view for the specific author with a primary key field of <id>. For example, the URL for the 11th author added to the list will be /catalog/author/11.
    path("author/<int:pk>", views.AuthorDetailView.as_view(), name="author-detail"),
    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    path(
        "borrowed/", views.LoanedBooksByAllUsersListView.as_view(), name="all-borrowed"
    ),
    path(
        "book/<uuid:pk>/renew/", views.renew_book_librarian, name="renew-book-librarian"
    ),
    
    # MDN_URL/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Forms#url_configurations
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),

    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]
