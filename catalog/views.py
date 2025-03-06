from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from .models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get("num_visits", 0)
    num_visits += 1
    request.session["num_visits"] = num_visits

    genre_counts = {
        "children": Genre.objects.filter(name__icontains="children").count(),
        "fiction": Genre.objects.filter(name__icontains="fiction").count(),
        "science": Genre.objects.filter(name__icontains="science").count(),
    }

    # chained filters are "AND"ed together, resulting in the "intersection" or "conjunction", but I wanted
    # the "OR"ed result (or "disjunction" or "union") so I used the Q object (note the added import above)
    # https://docs.djangoproject.com/en/5.0/topics/db/queries/#complex-lookups-with-q-objects
    scien_books_count = Book.objects.filter(
        Q(title__icontains="scien") | Q(summary__icontains="scien")
    ).count()

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "genre_counts": genre_counts,
        "scien_books_count": scien_books_count,
        "num_visits": num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)


from django.views import generic


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

    # examples of customizations we don't currently need
    # context_object_name = 'book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    #
    # overriding class methods
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    #
    # We might also override get_context_data() in order to pass additional context variables to
    # the template (e.g. the list of books is passed by default).
    # The fragment below shows how to add a variable named some_data to the
    # context (it would then be available as a template variable).
    # def get_context_data(self, **kwargs):
    #     # When doing this it is important to follow the pattern used above:
    #     # First get the existing context from our superclass.
    #     # Then add your new context information.
    #     # Then return the new (updated) context.
    #
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class LoanedBooksByAllUsersListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_all.html"
    paginate_by = 10
    permission_required = ('catalog.can_mark_returned', 'catalog.change_book')

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o").order_by(
            "due_back"
        )
