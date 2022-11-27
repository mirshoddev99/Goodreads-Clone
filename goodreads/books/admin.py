from django.contrib import admin
from .models import Book, Author, BookReview, Bookauthor

# Custom class for displaying models on Admin panel
class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')                        # Search property
    list_filter = ['title']                                 # Filter property
    list_display = ['title', 'isbn']         # Display property for details




admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(BookReview)
admin.site.register(Bookauthor)
